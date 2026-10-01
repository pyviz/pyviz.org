"""Load the tools catalog (tools.yml, sponsors.yml, builtons.yml).

Shared by the badge builder and the Sphinx build so both see the same
normalized package entries.
"""

from pathlib import Path

import yaml

TOOLS_DIR = Path(__file__).resolve().parent

DEFAULT_BADGES = ["pypi", "conda"]

# Badges implied by the presence of a package field.
IMPLIED_BADGES = {
    "conda_channel": "conda",
    "sponsors": "sponsor",
    "builtons": "builton",
    "site": "site",
    "dormant": "dormant",
}


def _load_yaml(name):
    with (TOOLS_DIR / name).open() as f:
        return yaml.safe_load(f)


def normalize_package(entry):
    """Return a copy of a tools.yml package entry with all derived fields set."""
    package = dict(entry)
    user, sep, name = package["repo"].partition("/")
    if not (user and sep and name) or "/" in name:
        raise ValueError(f"'repo' must be in the form 'org/name', got: {entry!r}")
    package["user"], package["name"] = user, name
    package.setdefault("pypi_name", name)
    package.setdefault("conda_package", name)

    if package.get("badges"):
        badges = [badge.strip() for badge in package["badges"].split(",")]
    else:
        badges = list(DEFAULT_BADGES)
    for field, badge in IMPLIED_BADGES.items():
        if package.get(field) and badge not in badges:
            badges.append(badge)
    package["badges"] = badges

    if "rtd" in badges:
        package.setdefault("rtd_name", name)
    if "conda" in badges:
        package.setdefault("conda_channel", "anaconda")
    if "site" in badges:
        if "site" in package:
            protocol, sep, site = package["site"].rstrip("/").partition("://")
            if not sep:
                protocol, site = "https", protocol
            package["site_protocol"], package["site"] = protocol, site
        else:
            package["site_protocol"], package["site"] = "https", f"{name}.org"
    return package


def load_sections():
    """Return the tools.yml sections, with normalized packages."""
    sections = _load_yaml("tools.yml")
    for section in sections:
        section["packages"] = [normalize_package(p) for p in section["packages"]]
    return sections


def iter_packages(sections):
    for section in sections:
        yield from section["packages"]


def load_sponsors():
    return _load_yaml("sponsors.yml")


def load_builtons():
    return _load_yaml("builtons.yml")
