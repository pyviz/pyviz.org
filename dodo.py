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

cache_param = {
    'name': 'cache',
    'long': 'cache',
    'type': bool,
    'default': True,
    'inverse': 'nocache',
}

def task_build_website():
    """Build website using nbsite"""
    return {'actions': [
        "echo building cache: %(cache)s",
        "python tools/conda_downloads.py",
        "BUILD_CACHE=%(cache)s python tools/build.py",
        "mv tools/index.rst doc/tools.rst",
        "nbsite generate-rst --org pyviz --project-name pyviz --examples notebooks",  # noqa
        "nbsite build --what=html --output=builtdocs",
    ], 'params': [cache_param]}
