import sys
from datetime import date
from pathlib import Path

from jinja2 import Template
from markdown import markdown

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS_DIR))

# catalog lives in tools/, which is only importable once added to sys.path.
from catalog import load_builtons, load_sections, load_sponsors  # noqa: E402

project = "PyViz"
author = "PyViz authors"
copyright = "2019, PyViz authors"
version = release = "0.0.1"

extensions = ["myst_parser"]
exclude_patterns = ["_build"]

html_theme = "alabaster"
html_static_path = ["_static"]
html_favicon = "_static/favicon.ico"
html_baseurl = "https://pyviz.org/"
html_copy_source = False
# Keep the sidebar order of the previous alabaster version, search last.
html_sidebars = {
    "**": ["about.html", "navigation.html", "relations.html", "searchbox.html"]
}
html_theme_options = {
    "logo": "logo.png",
    "logo_name": False,
    "page_width": "90%",
    "font_family": "Ubuntu, sans-serif",
    "font_size": "0.9em",
    "link": "#347ab4",
    "link_hover": "#1c4669",
    "extra_nav_links": {
        "Github": "https://github.com/pyviz/pyviz.org",
    },
    "show_powered_by": False,
}

TOOLS_PLACEHOLDER = "<!-- tools-table -->"


def render_tools_table():
    sections = load_sections()
    for section in sections:
        if section.get("intro"):
            section["intro"] = markdown(section["intro"])
    template = Template((TOOLS_DIR / "template.html").read_text())
    today = date.today()
    return template.render(
        config=sections,
        sponsors=load_sponsors(),
        builtons=load_builtons(),
        date=f"{today:%B} {today.day}, {today.year}",
    )


def insert_tools_table(app, docname, source):
    if docname != "tools":
        return
    if TOOLS_PLACEHOLDER not in source[0]:
        raise ValueError(f"{TOOLS_PLACEHOLDER} not found in tools.md")
    source[0] = source[0].replace(TOOLS_PLACEHOLDER, render_tools_table())


def setup(app):
    app.connect("source-read", insert_tools_table)
    return {"parallel_read_safe": True}
