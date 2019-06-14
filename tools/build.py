#!/usr/bin/env python

import os
import sys
from jinja2 import Template
from yaml import safe_load
import requests


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'tools.yml')) as f:
    config = safe_load(f)

existing = {package['repo'].split('/')[1].lower(): package for section in config for package in section['packages']}

registry = []

for package in registry:
    # FIXME: Not all repo name is actual package name.
    pkg_name = package['name'].lower()

    if pkg_name in existing:
        entry = existing[pkg_name]
    else:
        entry = {}
    if 'repo' not in entry:
        if 'github.com' in package['repo_url']:
            entry['repo'] = package['repo_url'].split('github.com/')[1]
        else:
            print("Skipping package {0} which is not on GitHub".format(package['name']))
    if 'pypi_name' not in entry:
        entry['pypi_name'] = package['pypi_name']
    if 'badges' not in entry:
        entry['badges'] = 'travis, coveralls, rtd, pypi, conda'
    # if pkg_name not in existing:
    #     affiliated['packages'].append(entry)

for section in config:
    for package in section['packages']:
        package['user'], package['name'] = package['repo'].split('/')
        package['badges'] = [x.strip() for x in package['badges'].split(',')]
        package['conda_package'] = package.get('conda_package', package['name'])
        if 'rtd' in package['badges'] and 'rtd_name' not in package:
            package['rtd_name'] = package['name']
        if 'pypi' in package['badges'] and 'pypi_name' not in package:
            package['pypi_name'] = package['name']
        if 'appveyor' in package['badges'] and 'appveyor_project' not in package:
            package['appveyor_project'] = package['repo']
        if 'circleci' in package['badges'] and 'circleci_project' not in package:
            package['circleci_project'] = package['repo']
        if 'travis' in package['badges'] and 'travis_project' not in package:
            package['travis_project'] = package['repo']
        if 'conda' in package['badges'] and 'conda_channel' not in package:
            package['conda_channel'] = 'anaconda'
        if 'site' in package['badges'] and 'site' not in package:
            package['site'] = '{}.org'.format(package['name'])
        if 'site' in package['badges'] and 'site_protocol' not in package:
            package['site_protocol'] = 'https'


template = Template(open(os.path.join(here, 'template.html'), 'r').read())

with open(os.path.join(here, 'index.rst'), 'w') as f:
    f.write("All Tools\n")
    f.write("=========\n\n")
    f.write(".. raw:: html\n\n")
    f.write(template.render(config=config))
