"""Build the badges shown on the "All Tools" page into doc/_static/cache.

Failure policy, once retries are exhausted:

- stars, pypi_downloads and conda_downloads are fresh-only: an error badge
  is written, so the page never shows a silently stale number.
- contributors and license are reusable: the previously cached file is kept
  if it exists and is itself a valid badge, otherwise an error badge is
  written.

Badge errors never fail the script, configuration errors do.
"""

import argparse
import html
import math
import re
import sys
import time
from dataclasses import dataclass
from datetime import date, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import quote, urlsplit

import colorcet as cc
import polars as pl
import requests
from tenacity import retry, retry_if_result, stop_after_attempt

from catalog import iter_packages, load_sections

CACHE_DIR = Path(__file__).resolve().parent.parent / "doc" / "_static" / "cache"

USER_AGENT = "pyviz.org-badges (+https://github.com/pyviz/pyviz.org)"
TIMEOUT = 30
MAX_ATTEMPTS = 4
BACKOFF = 5  # seconds, doubled after each attempt
MAX_WAIT = 120
RETRY_STATUSES = {408, 429, 500, 502, 503, 504}
# Once a host failed this many requests in a row, stop retrying it so an
# outage doesn't turn into hours of backoff.
GIVE_UP_AFTER = 5
# Minimum seconds between two requests to the same host. pypistats allows
# 30 requests per minute per IP, retries included, so stay well below.
HOST_INTERVALS = {"pypistats.org": 3.0}

SHIELDS = "https://img.shields.io"
PYPISTATS_URL = "https://pypistats.org/api/packages/{name}/recent?period=month"
CONDA_URL = (
    "https://anaconda-package-data.s3.amazonaws.com/conda/monthly/"
    "{year}/{year}-{month:02d}.parquet"
)

# Messages of shields error badges (core/base-service/errors.js and
# check-error-response.js), plus our own error reasons.
ERROR_MESSAGES = {
    "inaccessible",
    "invalid",
    "invalid parameter",
    "invalid response data",
    "improperly configured",
    "internal error",
    "not found",
    "rate limited",
    "rate limited by upstream service",
    "unavailable",
}
# Shields services customize "not found", e.g. "repo not found".
ERROR_SUFFIXES = ("not found",)
ERROR_PREFIXES = ("unparseable ",)

# Shields named colors, used by the local fallback renderer.
NAMED_COLORS = {
    "brightgreen": "4c1",
    "green": "97ca00",
    "yellowgreen": "a4a61d",
    "yellow": "dfb317",
    "red": "e05d44",
    "lightgrey": "9f9f9f",
}

CONDA_COLORS = [color.lstrip("#") for color in cc.palette_n.rainbow[-20:80:-1]]
CONDA_COLORMAP_TOP = 1e6


@dataclass(frozen=True)
class Kind:
    name: str
    # Whether a previous valid badge may be kept when fetching fails.
    reusable: bool
    # Package field identifying what to fetch.
    target: str
    # Only built for packages listing this badge, or for all if None.
    requires: str | None = None
    shields_url: str | None = None


# Override the label with a space to disable it and reduce the badge size.
KINDS = {
    kind.name: kind
    for kind in [
        Kind(
            "stars",
            reusable=False,
            target="repo",
            shields_url=f"{SHIELDS}/github/stars/{{}}.svg?style=flat&logo=github&color=blue&label=%20",
        ),
        Kind(
            "contributors",
            reusable=True,
            target="repo",
            shields_url=f"{SHIELDS}/github/contributors/{{}}.svg?style=flat&logo=github&color=blue&label=%20",
        ),
        Kind(
            "license",
            reusable=True,
            target="pypi_name",
            requires="pypi",
            shields_url=f"{SHIELDS}/pypi/l/{{}}.svg?label",
        ),
        Kind("pypi_downloads", reusable=False, target="pypi_name", requires="pypi"),
        Kind(
            "conda_downloads", reusable=False, target="conda_package", requires="conda"
        ),
    ]
}


@dataclass(frozen=True)
class Badge:
    kind: Kind
    name: str
    target: str

    @property
    def path(self):
        return CACHE_DIR / f"{self.name}_{self.kind.name}_badge.svg"

    def __str__(self):
        return f"{self.kind.name} {self.name}"


@dataclass(frozen=True)
class Fetched:
    svg: str
    # None when the badge is valid, otherwise a short reason.
    error: str | None = None


def badge_title(svg):
    """Return the "label: message" text of a badge, or None if it has none."""
    match = re.search(r"<title>(.*?)</title>", svg, re.DOTALL)
    if match:
        return html.unescape(match.group(1)).strip()
    # Shields omits the <title> of linked badges (e.g. GitHub stars), fall
    # back to the visible texts, each drawn several times (shadow, text).
    texts = re.findall(r"<text[^>]*>(.*?)</text>", svg, re.DOTALL)
    texts = [html.unescape(text).strip() for text in dict.fromkeys(texts)]
    return ": ".join(filter(None, texts)) or None


def error_message(svg):
    """Return the error message of a badge, or None if it is a valid badge."""
    title = badge_title(svg)
    if title is None:
        return "unparseable badge"
    # Labelled badges have a "label: message" title.
    candidates = [title, title.partition(": ")[2]]
    for message in filter(None, candidates):
        if (
            message in ERROR_MESSAGES
            or message.endswith(ERROR_SUFFIXES)
            or message.startswith(ERROR_PREFIXES)
        ):
            return message
    return None


def is_error_badge(svg):
    return error_message(svg) is not None


def is_transient_error(message):
    return not (message.endswith(ERROR_SUFFIXES) or message == "invalid parameter")


class Client:
    """HTTP client retrying 429/5xx and network errors with backoff."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT
        self.failures_in_a_row = {}
        self.last_request = {}

    def get(self, url, *, method="GET", retry_if=None):
        """Return the last response, or None if no response was received."""
        host = urlsplit(url).hostname
        # Once a host failed repeatedly, make one attempt only, so an outage
        # doesn't turn into hours of backoff.
        attempts = (
            1 if self.failures_in_a_row.get(host, 0) >= GIVE_UP_AFTER else MAX_ATTEMPTS
        )

        def failure_reason(response):
            if response is None:
                return "request failed"
            if response.status_code in RETRY_STATUSES:
                return f"HTTP {response.status_code}"
            if retry_if is not None:
                return retry_if(response)
            return None

        def wait(state):
            response = state.outcome.result()
            return _retry_after(response) or BACKOFF * 2 ** (state.attempt_number - 1)

        def log_retry(state):
            delay = state.next_action.sleep
            reason = failure_reason(state.outcome.result())
            print(f"    {reason}, retrying in {delay:g}s")

        @retry(
            retry=retry_if_result(
                lambda response: failure_reason(response) is not None
            ),
            wait=wait,
            stop=stop_after_attempt(attempts),
            before_sleep=log_retry,
            # Return the last response instead of raising RetryError.
            retry_error_callback=lambda state: state.outcome.result(),
        )
        def attempt():
            self._throttle(host)
            try:
                response = self.session.request(method, url, timeout=TIMEOUT)
            except requests.RequestException as exc:
                print(f"    {type(exc).__name__}: {exc}")
                return None
            return response

        response = attempt()
        if failure_reason(response) is not None:
            self.failures_in_a_row[host] = self.failures_in_a_row.get(host, 0) + 1
        else:
            self.failures_in_a_row[host] = 0
        return response

    def _throttle(self, host):
        interval = HOST_INTERVALS.get(host)
        if interval is not None:
            elapsed = time.monotonic() - self.last_request.get(host, -math.inf)
            if elapsed < interval:
                time.sleep(interval - elapsed)
            self.last_request[host] = time.monotonic()


def _retry_after(response):
    value = response.headers.get("Retry-After") if response is not None else None
    if not value:
        return None
    try:
        wait = float(value)
    except ValueError:
        try:
            wait = parsedate_to_datetime(value).timestamp() - time.time()
        except TypeError, ValueError:
            return None
    return min(max(wait, 0), MAX_WAIT)


def _is_svg(response):
    return response.headers.get("Content-Type", "").startswith("image/svg")


# Static badges


def _escape(text):
    return quote(text.replace("-", "--").replace("_", "__"), safe="")


def local_badge(label, message, color):
    """Render a shields-like flat badge, used when shields is unreachable."""
    color = NAMED_COLORS.get(color, color)
    title = html.escape(f"{label}: {message}" if label.strip() else message)
    label, message = html.escape(label.strip()), html.escape(message)
    label_width = len(label) * 7 + 10 if label else 0
    message_width = len(message) * 7 + 10
    width = label_width + message_width
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="20" '
        f'role="img" aria-label="{title}"><title>{title}</title>'
        f'<clipPath id="r"><rect width="{width}" height="20" rx="3" fill="#fff"/>'
        f'</clipPath><g clip-path="url(#r)">'
        f'<rect width="{label_width}" height="20" fill="#555"/>'
        f'<rect x="{label_width}" width="{message_width}" height="20" fill="#{color}"/>'
        f'</g><g fill="#fff" text-anchor="middle" '
        f'font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">'
        f'<text x="{label_width / 2}" y="14">{label}</text>'
        f'<text x="{label_width + message_width / 2}" y="14">{message}</text>'
        f"</g></svg>"
    )


def static_badge(client, label, message, color):
    url = f"{SHIELDS}/badge/{_escape(label)}-{_escape(message)}-{color}.svg"
    response = client.get(url)
    if response is not None and response.status_code == 200 and _is_svg(response):
        return response.text
    print("    shields unreachable, rendering the badge locally")
    return local_badge(label, message, color)


def error_badge(client, label, reason):
    return Fetched(static_badge(client, label, reason, "lightgrey"), reason)


# Shields-backed kinds


def _transient_error(response):
    """Return the message of a transient shields error badge, else None."""
    if not _is_svg(response):
        return f"HTTP {response.status_code}, not a badge"
    message = error_message(response.text)
    if message is not None and is_transient_error(message):
        return message
    return None


def fetch_shields(client, badge):
    url = badge.kind.shields_url.format(badge.target)
    response = client.get(url, retry_if=_transient_error)
    if response is None or not _is_svg(response):
        return error_badge(client, " ", "unavailable")
    svg = response.text
    message = error_message(svg)
    if message is None and response.status_code != 200:
        message = f"HTTP {response.status_code}"
    return Fetched(svg, message)


# PyPI downloads


def metric(n):
    """Port of shields' metric() number formatting (text-formatters.js)."""
    prefixes = "kMGTPEZY"
    for i in reversed(range(len(prefixes))):
        limit = 1000 ** (i + 1)
        if n >= limit:
            scaled = n / limit
            if scaled < 10:
                one_decimal = f"{scaled:.1f}"
                if not one_decimal.endswith("0"):
                    return f"{one_decimal}{prefixes[i]}"
            # JS Math.round rounds halves up, Python's round() to even.
            rounded = math.floor(scaled + 0.5)
            if rounded < 1000:
                return f"{rounded}{prefixes[i]}"
            return f"1{prefixes[i + 1]}"
    return str(n)


def download_color(n):
    """Port of shields' downloadCount() color (color-formatters.js)."""
    if n <= 0:
        return "red"
    if n < 10:
        return "yellow"
    if n < 100:
        return "yellowgreen"
    if n < 1000:
        return "green"
    return "brightgreen"


def fetch_pypi_downloads(client, badge):
    response = client.get(PYPISTATS_URL.format(name=badge.target.lower()))
    if response is None:
        return error_badge(client, "pypi", "unavailable")
    if response.status_code == 404:
        return error_badge(client, "pypi", "not found")
    if response.status_code == 429:
        return error_badge(client, "pypi", "rate limited")
    if response.status_code != 200:
        return error_badge(client, "pypi", "unavailable")
    try:
        downloads = int(response.json()["data"]["last_month"])
    except ValueError, KeyError, TypeError:
        return error_badge(client, "pypi", "invalid")
    message = f"{metric(downloads)}/month"
    return Fetched(static_badge(client, "pypi", message, download_color(downloads)))


# Conda downloads


def conda_data_url(client):
    """Return the URL of the latest monthly parquet file, or None."""
    month = date.today().replace(day=1)
    for _ in range(2):
        month = (month - timedelta(days=1)).replace(day=1)
        url = CONDA_URL.format(year=month.year, month=month.month)
        response = client.get(url, method="HEAD")
        if response is None:
            return None
        if response.status_code == 200:
            return url
        print(f"  {url}: HTTP {response.status_code}")
        if response.status_code != 404:
            return None
    return None


def load_conda_downloads(client, names):
    """Return the monthly downloads of each package, or None if unavailable."""
    url = conda_data_url(client)
    if url is None:
        return None
    print(f"  Loading {url}")
    # String columns are dictionary-encoded, hence the cast.
    pkg_name = pl.col("pkg_name").cast(pl.String).str.to_lowercase()
    try:
        downloads = (
            pl.scan_parquet(url)
            .select(pkg_name, "counts")
            .filter(pl.col("pkg_name").is_in(names))
            .group_by("pkg_name")
            .agg(pl.col("counts").sum())
            .collect()
        )
    except (pl.exceptions.PolarsError, OSError) as exc:
        print(f"  Failed to load conda downloads: {exc}")
        return None
    return dict(downloads.iter_rows())


def conda_color(downloads):
    if downloads <= 0:
        return CONDA_COLORS[0]
    if downloads > CONDA_COLORMAP_TOP:
        return CONDA_COLORS[-1]
    step = len(CONDA_COLORS) / math.log10(CONDA_COLORMAP_TOP)
    index = min(int(math.log10(downloads) * step), len(CONDA_COLORS) - 1)
    return CONDA_COLORS[index]


def conda_message(downloads):
    if downloads > 1e6:
        count = f"{int(downloads / 1e6)}M"
    elif downloads > 1e3:
        count = f"{int(downloads / 1e3)}k"
    else:
        count = str(downloads)
    return f"{count}/month"


def build_conda_downloads(client, badges):
    names = sorted({badge.target.lower() for badge in badges})
    downloads = load_conda_downloads(client, names)
    for badge in badges:
        print(f"  {badge}")
        if downloads is None:
            yield badge, error_badge(client, "conda", "unavailable")
        else:
            count = downloads.get(badge.target.lower(), 0)
            svg = static_badge(
                client, "conda", conda_message(count), conda_color(count)
            )
            yield badge, Fetched(svg)


# Orchestration


def collect_badges(sections, kinds):
    """Return the badges to build, deduplicated by output file."""
    badges = {}
    for package in iter_packages(sections):
        for kind in kinds:
            if kind.requires is not None and kind.requires not in package["badges"]:
                continue
            badge = Badge(kind, package["name"], package[kind.target])
            previous = badges.setdefault(badge.path, badge)
            if previous != badge:
                raise ValueError(
                    f"{badge.path.name} is built from both {previous.target!r} "
                    f"and {badge.target!r}, set the same {kind.target!r} on "
                    f"every {package['repo']!r} entry"
                )
    return list(badges.values())


def build(client, badges):
    for kind in KINDS.values():
        kind_badges = [badge for badge in badges if badge.kind == kind]
        if not kind_badges:
            continue
        print(f"Building {len(kind_badges)} {kind.name} badges")
        if kind.name == "conda_downloads":
            yield from build_conda_downloads(client, kind_badges)
            continue
        fetch = fetch_pypi_downloads if kind.name == "pypi_downloads" else fetch_shields
        for badge in kind_badges:
            print(f"  {badge}")
            yield badge, fetch(client, badge)


def reusable_previous(badge):
    if not (badge.kind.reusable and badge.path.exists()):
        return False
    return not is_error_badge(badge.path.read_text(errors="replace"))


def write_badges(client, badges):
    """Build and write the badges, return the errors and reused badges."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    errors, reused = [], []
    for badge, fetched in build(client, badges):
        if fetched.error is None:
            badge.path.write_text(fetched.svg)
        elif reusable_previous(badge):
            print(f"    {fetched.error}, keeping the previous badge")
            reused.append((badge, fetched.error))
        else:
            print(f"    {fetched.error}")
            badge.path.write_text(fetched.svg)
            errors.append((badge, fetched.error))
    return errors, reused


def parse_kinds(value):
    names = [name.strip() for name in value.split(",") if name.strip()]
    unknown = sorted(set(names) - KINDS.keys())
    if unknown:
        raise argparse.ArgumentTypeError(
            f"unknown kinds {', '.join(unknown)}, choose from {', '.join(KINDS)}"
        )
    return [KINDS[name] for name in names]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--kinds",
        type=parse_kinds,
        default=list(KINDS.values()),
        help=f"comma-separated badge kinds to build (default: {','.join(KINDS)})",
    )
    args = parser.parse_args()
    # Show progress live in CI logs, where stdout is not a terminal.
    sys.stdout.reconfigure(line_buffering=True)

    badges = collect_badges(load_sections(), args.kinds)
    errors, reused = write_badges(Client(), badges)

    fresh = len(badges) - len(errors) - len(reused)
    print(
        f"\n{len(badges)} badges: {fresh} fresh, {len(reused)} reused (stale), "
        f"{len(errors)} errors"
    )
    for title, entries in [("Errors", errors), ("Reused (stale)", reused)]:
        if entries:
            print(f"\n{title}:")
            for badge, reason in entries:
                print(f"  {badge}: {reason}")


if __name__ == "__main__":
    main()
