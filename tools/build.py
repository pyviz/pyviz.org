#!/usr/bin/env python
import os
from jinja2 import Template
from yaml import safe_load
from markdown import markdown


here = os.path.abspath(os.path.dirname(__file__))

print("Opening config file")
with open(os.path.join(here, 'tools.yml')) as f:
    config = safe_load(f)

for section in config:
    print(f"Building {section.get('name', '')}")
    if section.get('intro'):
        section['intro'] = markdown(section['intro'])
    for package in section['packages']:
        try:
            package['user'], package['name'] = package['repo'].split('/')
        except:
            raise Warning('Package.repo is not in correct format', package)
            continue
        package['conda_package'] = package.get('conda_package', package['name'])
        package['pypi_name'] = package.get('pypi_name', package['name'])

        if package.get('badges'):
            package['badges'] = [x.strip() for x in package['badges'].split(',')]
        else:
            package['badges'] = ['pypi', 'conda']
        if package.get('conda_channel') and 'conda' not in package['badges']:
            package['badges'].append('conda')
        if package.get('sponsors') and 'sponsor' not in package['badges']:
            package['badges'].append('sponsor')
        if package.get('site') and 'site' not in package['badges']:
            package['badges'].append('site')
        if package.get('dormant') and 'dormant' not in package['badges']:
            package['badges'].append('dormant')

        if 'rtd' in package['badges'] and 'rtd_name' not in package:
            package['rtd_name'] = package['name']
        if 'conda' in package['badges'] and 'conda_channel' not in package:
            package['conda_channel'] = 'anaconda'
        if 'site' in package['badges']:
            if 'site' not in package:
                package['site'] = '{}.org'.format(package['name'])
                package['site_protocol'] = 'https'
            else:
                package['site_protocol'], package['site'] = package['site'].rstrip('/').split('://')

with open(os.path.join(here, 'sponsors.yml')) as f:
    sponsors = safe_load(f)

template = Template(open(os.path.join(here, 'template.html'), 'r').read())

with open(os.path.join(here, 'index.rst'), 'w') as f:
    f.write("All Tools\n")
    f.write("=========\n\n")
    f.write(".. mdinclude:: tools.md\n\n")
    f.write(".. raw:: html\n\n")
    f.write(template.render(config=config, sponsors=sponsors))
