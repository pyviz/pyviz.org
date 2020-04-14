#!/usr/bin/env python
"""
Run this script at the beginning of each month to build new conda downloads badges
from the previous month.
"""

import os
from yaml import safe_load
import requests
import datetime
import intake
import colorcet as cc
import numpy as np


here = os.path.abspath(os.path.dirname(__file__))
cache_path = os.path.join(here, '..', 'doc', '_static', 'cache')
cat = intake.open_catalog('https://raw.githubusercontent.com/ContinuumIO/anaconda-package-data/master/catalog/anaconda_package_data.yaml')

colors = cc.palette_n.rainbow[-20:80:-1]
top_of_colormap = 1e6
step = len(colors) /np.log10(top_of_colormap)

today = datetime.date.today()
first = today.replace(day=1)
last_month = first - datetime.timedelta(days=1)
try:
    monthly = cat.anaconda_package_data_by_month(year=last_month.year, month=last_month.month,
                                                 columns=['pkg_name', 'counts']).to_dask()
except:
    # if the last month isn't available, get the month before
    month_before = last_month.replace(day=1) - datetime.timedelta(days=1)
    monthly = cat.anaconda_package_data_by_month(year=month_before.year, month=month_before.month,
                                                columns=['pkg_name', 'counts']).to_dask()
per_package_downloads = monthly.groupby('pkg_name').sum().compute()

if not os.path.exists(cache_path):
    os.mkdir(cache_path)

def get_conda_badge(conda_package):
    conda_package = conda_package.lower()
    if conda_package in per_package_downloads.index:
        downloads = per_package_downloads.counts.loc[conda_package]
    else:
        downloads = 0

    if downloads == 0:
        color_index = 0
    elif downloads > top_of_colormap:
        color_index = -1
    else:
        color_index = int(np.log10(downloads) * step)
    color = colors[color_index][1:]

    if downloads > 1e6:
        downloads = '{}M'.format(int(downloads/1e6))
    elif downloads > 1e3:
        downloads = '{}k'.format(int(downloads/1e3))
    else:
        downloads = int(downloads)

    return  f"https://img.shields.io/badge/conda-{downloads}/month-{color}.svg"

with open(os.path.join(here, 'tools.yml')) as f:
    config = safe_load(f)

for section in config:
    print(f"Building conda downloads badge for: {section['name']}")
    for package in section['packages']:
        try:
            package['user'], package['name'] = package['repo'].split('/')
        except:
            raise Warning('Package.repo is not in correct format', package)
            continue
        url = get_conda_badge(package.get('conda_package', package['name']))
        rendered_url = url
        r = requests.get(rendered_url)
        with open(os.path.join(cache_path, f"{package['name']}_conda_downloads_badge.svg"), 'wb') as f:
            f.write(r.content)
