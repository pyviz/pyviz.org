#!/usr/bin/env python

import subprocess
import shutil
from jinja2 import Template
from yaml import load

with open('dashboard.yml') as f:
    config = load(f)

for section in config:
    for package in section['packages']:
        package['user'], package['name'] = package['repo'].split('/')
        package['badges'] = [x.strip() for x in package['badges'].split(',')]
        if 'rtd_name' not in package:
            package['rtd_name'] = package['name']
        if 'pypi_name' not in package:
            package['pypi_name'] = package['name']
        if 'appveyor' in package['badges'] and 'appveyor_project' not in package:
            package['appveyor_project'] = package['repo']

template = Template(open('template.html', 'r').read())


with open('status.html', 'w') as f:
    f.write(template.render(config=config))
