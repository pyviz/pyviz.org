#!/usr/bin/env python

import os
import time
from yaml import safe_load
import requests

here = os.path.abspath(os.path.dirname(__file__))
cache_path = os.path.join(here, '..', 'doc', '_static', 'cache')
badge = os.getenv('BADGE')

cache = {
    "stars": "https://img.shields.io/github/stars/{repo}.svg?style=social",
    "contributors": "https://img.shields.io/github/contributors/{repo}.svg?style=social&logo=github",
    "pypi_downloads": "https://img.shields.io/pypi/dm/{pypi_name}.svg?label=pypi",
    "license": "https://img.shields.io/pypi/l/{pypi_name}.svg?label",
}
url = cache.get(badge)
if url is None:
    raise ValueError((f'{badge} not in {", ".join(cache.keys())}, use env '
                      'var BADGE to set.'))

# The pypi download badge cannot occasionally be properly fetched
# by shields and cached here. We list those that failed, so that
# in the template we can put the actual badge link rather than
# the cached one.
pypi_invalid_file = os.path.join(here, "pypi_invalid_badges.txt")
if os.path.exists(pypi_invalid_file):
  os.remove(pypi_invalid_file)

print(f"\nBuilding a cache of {badge} badges.\n")

if not os.path.exists(cache_path):
    os.mkdir(cache_path)

with open(os.path.join(here, 'tools.yml')) as f:
    config = safe_load(f)

for section in config:
    print(f"Building cache for {section.get('name', '')}")
    for package in section['packages']:
        try:
            package['user'], package['name'] = package['repo'].split('/')
        except:
            raise Warning('Package.repo is not in correct format', package)
        package['pypi_name'] = package.get('pypi_name', package['name'])

        print(f"  * package: {package.get('pypi_name', '')}")
        rendered_url = url.format(repo=package['repo'], pypi_name=package['pypi_name'])
        r = requests.get(rendered_url)
        content = r.content
        # Pypistats implements IP rate limiting, so let's slow things
        # down and retry a few times when failing.
        if badge == 'pypi_downloads':

            time.sleep(2.5)
            
            nb_retries = 4
            retry_duration = 5  # In seconds, multiplied by two after each retry.
            retry_count = 1
            while 'pypi: invalid' in r.text and retry_count <= nb_retries:
                print(f"PyPI badge returned as 'invalid'. Retrying after {retry_duration} seconds.")
                time.sleep(retry_duration)
                r = requests.get(rendered_url)
                content = r.content
                if retry_count == nb_retries:
                    print(f"Failed a getting a valid Pypi Downloads badge for {package['pypi_name']}.")
                    break
                retry_count += 1
                retry_duration *= 2
        
        if 'pypi: invalid' in r.text:
            with open(pypi_invalid_file, 'a') as f:
                f.write(package['pypi_name'] + '\n')

        with open(os.path.join(cache_path, f"{package['name']}_{badge}_badge.svg"), 'wb') as f:
            f.write(content)
