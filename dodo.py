import os

if "PYCTDEV_ECOSYSTEM" not in os.environ:
    os.environ["PYCTDEV_ECOSYSTEM"] = "conda"

from pyctdev import *  # noqa: api


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
        "conda env update -f environment-dev.yml -n pyviz",
    ]}


def task_build_website():
    """Build website using nbsite"""
    return {'actions': [
        "nbsite generate-rst --org pyviz --project-name pyviz --examples notebooks",  # noqa
        "nbsite build --what=html --output=builtdocs",
    ]}
