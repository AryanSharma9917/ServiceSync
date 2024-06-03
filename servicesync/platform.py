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

    def __repr__(self):
        return self.version

    def __eq__(self, version):
        return self.version == version

    def update_components(self, vers_config):
        self.version = vers_config.get('version')
        if not self.version:
            raise errors.NoVersionFoundError(
                """No platform version was defined in config file"""
            )

        vers_components = vers_config.get('components')
        if not vers_components:
            raise errors.NoComponentsDefinedError(
                f"""No components are defined for {self.version}"""
            )

        for component in self._components:
            match = next((c for c in vers_components if c.get('alias') == component), None)
            if not match:
                raise errors.ComponentUndefinedError(
                    f"""Component '{component['name']}' does not have a 
                    defined alias in config.yaml"""
                 )

            component.refs = match.get('refs')
            if not component.refs:
                raise errors.ComponentTagUndefinedError()

            component.hash = match.get('hash')
            if not component.hash:
                raise errors.ComponentRefsUndefinedError()
            
            component.location = match.get('url')
            if not component.url:
                raise errors.NoComponentLocationDefined()

    def fetch_components(self, repo_path, ssh_pub_key, ssh_priv_key):
        workspace = path.join(repo_path, self.name)
        for component in self._components:
            component.fetch(workspace, ssh_pub_key, ssh_priv_key)


class MicroService:
    """MicroService holds the microservice config and relevant
    functionality.
    """
    refs = None
    hash = None
    url = None
    
    def __init__(self, alias, url):
        self.alias = alias
        self.url = url

    def __repr__(self):
        return self.alias

    def __eq__(self, alias):
        return self.alias == alias

    def fetch(self, workspace, ssh_pub_key, ssh_priv_key, validate=False):
        """This function will try to create the workspace for the component
        that will be cloned. It will fetch the component and will export the
        environment variable that points to component cloned repository.
        """
        self._clone(workspace, ssh_pub_key, ssh_priv_key)
        if validate:
            self._export_env(workspace)

    def _clone(
        self,
        workspace,
        ssh_pub_key,
        ssh_priv_key,
        ssh_user='git',
        ssh_pass='',
    ):
        ws = util.create_workspace(workspace, self.alias)
        keypair = Keypair(
            username=ssh_user,
            pubkey=ssh_pub_key,
            privkey=ssh_priv_key,
            passphrase=ssh_pass,
        )

        try:
            cb = RemoteCallbacks(credentials=keypair)
            repo = clone_repository(
                url=self.url,
                path=ws,
                callbacks=cb,
            )
            try:
                repo.checkout(self.refs)
                print(f'Cloned {repo} to {ws}')
            except Exception as err:
                raise errors.CannotFetchRef(
                    f'Cannot fetch ref: {self.refs}'
                )
        except Exception as err:
                raise errors.CannotCloneRepository(
                    f'Cannot clone repository: {err}'
                )

    def _export_env(self, workspace):
        """Used to export the path of the cloned git repository.
        Useful in CI/CD platform pipelines.
        """
        _name = f'{self.alias}_WORKSPACE'.upper()
        environ[_name] = workspace
