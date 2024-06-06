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

def get_versions_paths(workspace_path, version):
    """Walks the specified directory where the platform versioning is located
    and will try to find all the directories that match a regex of v[0-9]+.
    e.g.: v1, v2, v3.
    :param workspace_path: string path to the workspace where the 
    configuration is located.
    :param version: string the specific version to search for.
    :return: a list of all yaml files present in the specified version
    directory.
    """
    reg_vers = re.compile(version.split('.')[0])
    vers_dir = next((path for path in listdir(workspace_path) if reg_vers.match(path)), None)

    if not vers_dir:
        raise errors.NoVersionFoundError(
            f"""No version directory for version: {version} was found in 
            {workspace_path}"""
        )

    vers_path = path.join(workspace_path, vers_dir)
    reg_vers_match = version.split('.')

    try:
        reg_vers_file = re.compile(f'{reg_vers_match[0]}.{reg_vers_match[1]}')
    except IndexError:
        raise errors.SemverNonCompliantError(
        f"""Semver non-compliant: The requested version ({version}) needs at
        least a minor version"""
      )

    versions = list(filter(lambda p: re.search(reg_vers_file, p), listdir(vers_path)))

    if not versions:
        raise errors.NoVersionFoundError(
            f"""No version {version} has been defined in path {vers_path}"""
        )

    return list(map(lambda p: path.join(vers_path, p), versions))

def filter_version(version, workspace):
    """Creates a new list of Platform objects that contain the YAML config for
    the desired 
    :param version: string the version to search for
    :param workspace: string full path to the workspace.
    :return platforms: 
    """
    platform = Platform(workspace)
    yaml_files = get_versions_paths(workspace, version)
    contents = list(open_file(f) for f in yaml_files)

    platforms = []
    match_vers = re.compile(version)
    for platform_version in [content for content in contents]:
        for vers in [v for v in platform_version]:
            # NOTE: this is where the filtering for the specific version can be
            # done, after we parsed all the major version files.
            if not (match_vers.match(vers['version'])):
                continue
            platform_copy = copy.deepcopy(platform)
            platform_copy.update_components(vers)
            platforms.append(platform_copy)

    if len(platforms) == 0:
        raise errors.NoVersionFoundError(
            f"""Version {version} was not found in {workspace}"""
        )

    return platforms

def tabulate_data(data, headers, table_type='fancy_grid'):
    print(tabulate(data, headers, tablefmt=table_type))

def create_workspace(components_workspace, name):
    """Creates a temporary workspace for a component to be cloned to, if  
    HURD_ARTIFACTS was not exported and no --path passed.
    """
    workspace = path.join(components_workspace, name)
    try:
        makedirs(workspace, mode=0o755, exist_ok=False)
    except OSError as err:
        raise errors.CannotCreateDirectory(
            f"""Cannot create temporary directory: {err}"""
        )

    return workspace
