from os import environ

import click

from servicesync import util
from servicesync import errors


def validate_version(ctx, param, value):
    """Custom validation for --version option"""
    if param.name == 'version' and not value:
        raise click.BadParameter('you need to pass a platform version')
    return value

def validate_workspace(ctx, param, value):
    """Custom validation for --workspace option"""
    if param.name == 'workspace' and not value:
        if not ('servicesync_WORKSPACE' in environ) or environ.get('servicesync_WORKSPACE') == '':
            raise click.UsageError("""pass --workspace or export 
                servicesync_WORKSPACE pointing to the full path directory where the 
                YAML platform version is located."""
            )
    return value

_global_options = [
    click.option(
        '--version',
        '-v',
        help='The specific platform version',
        callback=validate_version,
    ),
    click.option(
        '--workspace',
        '-w',
        envvar='servicesync_WORKSPACE',
        help="""The fullpath to the workspace containing the configuration and
        the platform versioning in yaml format.
        """,
        callback=validate_workspace,
        type=click.Path(exists=True),
    ),
]

_ssh_options = [
    click.option(
        '--ssh-pub-key',
        help='Full path to the ssh public key used to clone the repositories.',
        type=click.Path(),
        envvar='servicesync_PATH_PUBLIC_KEY',
    ),
    click.option(
        '--ssh-priv-key',
        help="""Full path to the ssh private key used to clone the 
        repositories.""",
        type=click.Path(),
        envvar='servicesync_PATH_PRIVATE_KEY',
    ),
    click.option(
        '--path',
        '-p',
        help="""Full path to where the artifacts should be cloned. If no path
         is given it will default to /tmp/${name-of-the-platform}""",
        type=click.Path(),
        default='/tmp',
        envvar='servicesync_ARTIFACTS',
    ),
]

def add_custom_options(options):
    """Wraps a defined function with global parameters"""
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options

@click.group()
def cli():
    pass

@cli.command(
    help="""Displays tabulated metadata about the pinned microservice platform
    version."""
)
@add_custom_options(_global_options)
def describe(version, workspace):
    _table_headers = ['Platform version', 'Alias', 'URL', 'Refs', 'Hash']
    platforms = util.filter_version(version, workspace)
    vers = []
    for version in [c for c in platforms]:
        for v in version._components:
            v._export_env(workspace=workspace)
            vers.append([version, v.alias, v.url, v.refs, v.hash])
    util.tabulate_data(vers, _table_headers)

@cli.command(
    help="""This command will start fetching all the repositories defined in a
    pinned version that match the specific version found. If multiple pinned
    versions match, it will fail with an error."""
)
@add_custom_options(_global_options + _ssh_options)
def fetch(version, workspace, path, ssh_pub_key, ssh_priv_key):
    platforms = util.filter_version(version, workspace)

    if len(platforms) > 1:
        raise errors.MultiplePlatformVersionsFound(
            f"""Multiple version found for {version}. Narrow down the search 
            to a minor version."""
        )
    platforms[0].fetch_components(path, ssh_pub_key, ssh_priv_key)

@cli.command(
    help="""This command will validate the defined platform pinned
    version by trying to fetch the refs described. If multiple versions match, 
    it will throw an exception."""
)
@add_custom_options(_global_options + _ssh_options)
def validate(version, workspace, path, ssh_pub_key, ssh_priv_key):
    pass

@cli.command(
    help="""This command will create a new git tag in the repositories defined
    by the YAML platform version config.
    Throws an exception if a a tag has been defined but does not match the one
    specified."""
)
@add_custom_options(_global_options + _ssh_options)
def tag(version, workspace, path, ssh_pub_key, ssh_priv_key):
    pass

if __name__ == '__main__':
    cli()