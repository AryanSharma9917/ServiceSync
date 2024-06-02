from os import path, environ

from pygit2 import clone_repository, Keypair, RemoteCallbacks

from . import util
from . import errors

class Platform:
    """Platform holds the general metadata and functionality about the 
    platform config.
    """
    name = None
    version = None
    _components = []

    def __init__(self, workspace):
        config_file = path.join(workspace, 'config.yaml')
        config = util.open_file(config_file)
        self._parse_config(config)

    def _parse_config(self, config):
        for data in config:
            self.name = data.get('name')
            if not self.name:
                raise errors.NoPlatformNameDefined(
                    """No platform name defined in config.yaml"""
                )

            for key, value in data.items():
                if key == 'name':
                    self.name = value
                    continue

                if key == 'components':
                    for component in value:
                        self._components.append(
                            MicroService(
                                alias=component.get('alias'),
                                url=component.get('url'),
                            )
                        )
