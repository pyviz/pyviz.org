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
        "BADGE=stars python tools/build_cache.py",
        "BADGE=contributors python tools/build_cache.py",
        "BADGE=license python tools/build_cache.py",
        "BADGE=pypi_downloads python tools/build_cache.py",
     ]}


def task_build_website():
    """Build website using nbsite"""
    return {'actions': [
        "python tools/build.py",
        "mv tools/index.rst doc/tools.rst",
        "nbsite generate-rst --org pyviz --project-name pyviz",  # noqa
        "nbsite build --what=html --output=builtdocs",
    ]}
