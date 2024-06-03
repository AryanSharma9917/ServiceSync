import re, copy
from os import path, listdir, makedirs

import yaml
from tabulate import tabulate

from .platform import Platform, MicroService
from . import errors


def open_file(config_file):
    """Opens a file and sends its contents to be consumer by the yaml library.
    :param config_file: string full path to the config file of the platform.
    :return: a generator object that contains the YAML spec of the file.
    """
    try:
        with open(config_file) as config:
            return yaml.safe_load_all(config.read())
    except FileNotFoundError:
        raise errors.NoConfigFileFound(
            f"""No 'config.yaml' file found in directory!"""
        )