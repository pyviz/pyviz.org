import subprocess
import shutil
from jinja2 import Template

PROJECTS = ['astropy/astropy',
            'astrofrog/reproject',
            'astrofrog/wcsaxes',
            'aplpy/aplpy',
            'astropy/montage-wrapper',
            'astropy/ccdproc',
            'astropy/imageutils',
            'astropy/photutils',
            'astropy/specutils',
            'gammapy/gammapy',
            'sncosmo/sncosmo',
            'weaverba137/pydl']

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
