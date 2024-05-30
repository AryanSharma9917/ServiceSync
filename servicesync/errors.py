class NoVersionFoundError(Exception):
    """This exception is thrown when
    a) there is no directory found for a specific version in the specified
    workspace. 
    b) there is YAML version file that matches the desired version.
    """
    pass


class NoComponentsDefinedError(Exception):
    """This exception is raised when there are no components defined under a
    platform.
    """
    pass


class NoPlatformVersionDefined(Exception):
    """This exception is raised when there is no platform version defined in
    config.yaml.
    """
    pass


class NoPlatformNameDefined(Exception):
    """This exception is raised when there is no platform name defined in
    config.yaml.
    """
    pass


class ComponentUndefinedError(Exception):
    """This exception is raised whenever an alias does not have a mapping
    component defined in the config version file.
    """
    pass


class ComponentTagUndefinedError(Exception):
    """This exception is raised whenever a tag is undefined on a component
    """
    pass


class ComponentRefsUndefinedError(Exception):
    """This exception is raised whenever a ref is undefined on a component
    """
    pass


class SemverNonCompliantError(Exception):
    """This exception is raised whenever the requested version does not 
    comply with semantic versioning.
    """
    pass


class MultiplePlatformVersionsFound(Exception):
    """This exception is raised whenever the version passed by the user 
    is too broad and returns multiple results. By definition you cannot fetch
    mutiple versions of a component.
    """
    pass


class NoConfigFileFound(Exception):
    """This exception is raised when the config.yaml is not found in the
    given directory.
    """
    pass


class NoComponentLocationDefined(Exception):
    """This exception is raised when there is no URL defined for the 
    component.
    """
    pass


class CannotCreateDirectory(Exception):
    """This exception is raised whenever the temporary workspace can not 
    be created. 
    """
    pass


class CannotCloneRepository(Exception):
    """This exception is raised whenever the specified repository cannot be
    cloned.
    """
    pass


class CannotFetchRef(Exception):
    """This exception is raised whenever the specified ref cannot be fetched.
    """
    pass
