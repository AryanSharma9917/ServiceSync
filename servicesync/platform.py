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