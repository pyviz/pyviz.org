import os

if "PYCTDEV_ECOSYSTEM" not in os.environ:
    os.environ["PYCTDEV_ECOSYSTEM"] = "conda"

from pyctdev import *  # noqa: api


here = os.path.abspath(os.path.dirname(__file__))


def task_ecosystem_setup():
    """Set up conda with updated version, and yes set to always"""
    return {'actions': [
        "conda config --set always_yes True",
        "conda update conda",
    ]}


def task_env_create():
    """Create environment from environment.yml and environment-dev.yml"""
    return {'actions': [
        "pip uninstall -y doit pyctdev",
        "conda env update -f environment.yml -n pyviz",
    ]}


def task_build_cache():
    """Build cache"""
    return {'actions': [
         "python tools/conda_downloads.py",
        'SECTION="Core" python tools/build_cache.py',
        'SECTION="High-Level Shared API" python tools/build_cache.py',
        'SECTION="High-Level" python tools/build_cache.py',
        'SECTION="Native-GUI" python tools/build_cache.py',
        'SECTION="Other InfoVis" python tools/build_cache.py',
        'SECTION="SciVis" python tools/build_cache.py',
        'SECTION="Geospatial" python tools/build_cache.py',
        'SECTION="Other domain-specific" python tools/build_cache.py',
        'SECTION="Large-data rendering" python tools/build_cache.py',
        'SECTION="Dashboarding" python tools/build_cache.py',
        'SECTION="Colormapping" python tools/build_cache.py',
        'SECTION="Dormant projects" python tools/build_cache.py',
     ]}


def task_build_website():
    """Build website using nbsite"""
    return {'actions': [
        "python tools/build.py",
        "mv tools/index.rst doc/tools.rst",
        "nbsite generate-rst --org pyviz --project-name pyviz --examples notebooks",  # noqa
        "nbsite build --what=html --output=builtdocs",
    ]}
