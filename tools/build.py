#!/usr/bin/env python

import os
from jinja2 import Template
from yaml import safe_load


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'tools.yml')) as f:
    config = safe_load(f)

with open(os.path.join(here, 'sponsors.yml')) as f:
    sponsors = safe_load(f)

for section in config:
    for package in section['packages']:
        package['user'], package['name'] = package['repo'].split('/')
        package['badges'] = [x.strip() for x in package['badges'].split(',')]
        package['conda_package'] = package.get('conda_package', package['name'])

        if package.get('conda_channel') and 'conda' not in package['badges']:
            package['badges'].append('conda')
        if package.get('sponsors') and 'sponsor' not in package['badges']:
            package['badges'].append('sponsor')
        if package.get('site') and 'site' not in package['badges']:
            package['badges'].append('site')

        if 'rtd' in package['badges'] and 'rtd_name' not in package:
            package['rtd_name'] = package['name']
        if 'pypi' in package['badges'] and 'pypi_name' not in package:
            package['pypi_name'] = package['name']
        if 'conda' in package['badges'] and 'conda_channel' not in package:
            package['conda_channel'] = 'anaconda'
        if 'site' in package['badges']:
            if 'site' not in package:
                package['site'] = '{}.org'.format(package['name'])
            if 'site_protocol' not in package:
                package['site_protocol'] = 'https'


template = Template(open(os.path.join(here, 'template.html'), 'r').read())

with open(os.path.join(here, 'index.rst'), 'w') as f:
    f.write("All Tools\n")
    f.write("=========\n\n")
    f.write(".. raw:: html\n\n")
    f.write(template.render(config=config, sponsors=sponsors))
