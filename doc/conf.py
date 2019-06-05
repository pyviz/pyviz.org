from nbsite.shared_conf import *

project = u'PyViz'
authors = u'PyViz authors'
copyright = u'\u00a9 2019, ' + authors
description = 'How to solve visualization problems with Python tools.'

version = release = '0.0.1'
extensions.extend(['m2r'])

html_static_path += ['_static']
html_favicon = 'favicon.ico'
html_theme_options = {
    'logo': 'logo.png',
    'logo_name': False,
    'page_width': '80%',
    'font_family': "Ubuntu, sans-serif",
    'font_size': '0.9em',
    'extra_nav_links': {'Github': 'https://github.com/pyviz/website'},
    'show_powered_by': False,
}

html_context.update({
    'PROJECT': project,
    'DESCRIPTION': description,
    'AUTHOR': authors,
    # WEBSITE_SERVER is optional for tests and local builds, but allows defining a canonical URL for search engines
    'WEBSITE_SERVER': 'https://pyviz.org',
})
