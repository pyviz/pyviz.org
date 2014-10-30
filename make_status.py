#!/usr/bin/env python

import subprocess
import shutil
from jinja2 import Template

PROJECTS = ['astropy/astropy',
            'astropy/package-template',
            'astropy/astroquery',
            'astrofrog/reproject',
            'astrofrog/wcsaxes',
            'aplpy/aplpy',
            'pyvirtobs/pyvo',
            'eteq/astropysics',
            'astropy/montage-wrapper',
            'astropy/ccdproc',
            'ejeschke/ginga',
            'astropy/imageutils',
            'astropy/photutils',
            'astropy/specutils',
            'astropy/pyregion',
            'gammapy/gammapy',
            'sncosmo/sncosmo',
            'spacetelescope/sphere',
            'weaverba137/pydl',
            'radio-astro-tools/pvextractor',
            'radio-astro-tools/spectral-cube']

rows = ""

packages = []

for package_url in PROJECTS:
    package = {}
    package['display_name'] = package_url
    package['user'], package['name'] = package_url.split('/')
    packages.append(package)

template = Template(open('template.html', 'r').read())

subprocess.call('git checkout gh-pages', shell=True)

with open('status.html', 'w') as f:
    f.write(template.render(packages=packages))

subprocess.call('git add status.html', shell=True)
subprocess.call('git commit -m "Latest build"', shell=True)
subprocess.call('git checkout master', shell=True)
