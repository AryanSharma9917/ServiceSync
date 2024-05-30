# ServiceSync

---
A declarative way to keep track of microservices under a common platform
version.

Usually, git submodules would be used to pin each microservice version in place
to the platform version.  

**NOTE**: This documentation is a _"work in progress"_.

#### Example
Let's call our e-commerce platform `ecom` which is comprised of the following
components:
- cart service
- payment gateway  
- persistence layer 
- billing service  

**NOTE**: Each version is a repository git tag.

`ecom v1.0`:
- `cart-service v1.0.1`  
- `payments-gateway v1.1.2`
- `persistence-layer v1.2.3`
- `billing-service v1.0.0`

In a git repository named `ecom-platform` a `config.yaml` file should exist
with the following contents:

```yaml
---
# name is the platform name
name: ecom 
# components are the microservices under the platform
components:
  # the alias is used to reference a component in a version file.
  - alias: cart
  # the url is used for pinning the alias to a git url
    url: git@github.com:ecom-org/cart-service.git
  - alias: payments
    url: git@github.com:ecom-org/payments-gateway.git
  - alias: persistence
    url: git@github.com:ecom-org/persistence-layer.git
  - alias: billing
    url: git@github.com:ecom-org/billing-service.git
```
A directory containing the major version e.g.: `v1` needs to be created. Inside
`v1` we need a file that has the following naming structure
`platform_name-major-version.minor-version.yaml` aka `ecom-v0.1.yaml` with the
following contents:

```yaml
---
# version describes the version of the platform
version: v1.0.0
components:
    - alias: cart
      refs: tags/v1.0.1
    - alias: payments
      refs: tags/v1.1.2
    - alias: persistence
      refs: tags/v1.2.3
    - alias: billing
      refs: tags/v1.0.0
```

#### Use

Describing a specific platform version:

Assuming the configuration from the [platform-test repo](https://github.com/codeflavor/platform-test).

```bash
$ HURD_WORKSPACE=~/projects/misc/platform-test/ python hurd.py describe -v v1.0.1
╒════════════════════╤═════════╤═════════════════════════════════════╤══════════════════╤══════════════════════════════════════════╕
│ Platform version   │ Alias   │ URL                                 │ Refs             │ Hash                                     │
╞════════════════════╪═════════╪═════════════════════════════════════╪══════════════════╪══════════════════════════════════════════╡
│ v1.0.1             │ test1   │ git@github.com:codeflavor/test1.git │ refs/tags/v1.0.1 │ 9701d9f3a555067f4a0fa5b61f9b7eafa78de9c2 │
├────────────────────┼─────────┼─────────────────────────────────────┼──────────────────┼──────────────────────────────────────────┤
│ v1.0.1             │ test2   │ git@github.com:codeflavor/test2.git │ refs/tags/v1.0.0 │ 854bf0434606da01b030e24ead572bc4196b4d3a │
├────────────────────┼─────────┼─────────────────────────────────────┼──────────────────┼──────────────────────────────────────────┤
│ v1.0.1             │ test3   │ git@github.com:codeflavor/test3.git │ refs/tags/v1.0.0 │ 5af8977d22913560b64c0c2b6001f914d097146b │
╘════════════════════╧═════════╧═════════════════════════════════════╧══════════════════╧══════════════════════════════════════════╛
```

Describing all minor/patch versions:

```bash
$ HURD_WORKSPACE=~/projects/misc/platform-test/ python hurd.py describe -v v1.0
╒════════════════════╤═════════╤═════════════════════════════════════╤══════════════════╤══════════════════════════════════════════╕
│ Platform version   │ Alias   │ URL                                 │ Refs             │ Hash                                     │
╞════════════════════╪═════════╪═════════════════════════════════════╪══════════════════╪══════════════════════════════════════════╡
│ v1.0.0             │ test1   │ git@github.com:codeflavor/test1.git │ refs/tags/v1.0.1 │ 9701d9f3a555067f4a0fa5b61f9b7eafa78de9c2 │
├────────────────────┼─────────┼─────────────────────────────────────┼──────────────────┼──────────────────────────────────────────┤
│ v1.0.0             │ test2   │ git@github.com:codeflavor/test2.git │ refs/tags/v1.0.0 │ 854bf0434606da01b030e24ead572bc4196b4d3a │
├────────────────────┼─────────┼─────────────────────────────────────┼──────────────────┼──────────────────────────────────────────┤
│ v1.0.0             │ test3   │ git@github.com:codeflavor/test3.git │ refs/tags/v1.0.0 │ 5af8977d22913560b64c0c2b6001f914d097146b │
├────────────────────┼─────────┼─────────────────────────────────────┼──────────────────┼──────────────────────────────────────────┤
│ v1.0.1             │ test1   │ git@github.com:codeflavor/test1.git │ refs/tags/v1.0.1 │ 9701d9f3a555067f4a0fa5b61f9b7eafa78de9c2 │
├────────────────────┼─────────┼─────────────────────────────────────┼──────────────────┼──────────────────────────────────────────┤
│ v1.0.1             │ test2   │ git@github.com:codeflavor/test2.git │ refs/tags/v1.0.0 │ 854bf0434606da01b030e24ead572bc4196b4d3a │
├────────────────────┼─────────┼─────────────────────────────────────┼──────────────────┼──────────────────────────────────────────┤
│ v1.0.1             │ test3   │ git@github.com:codeflavor/test3.git │ refs/tags/v1.0.0 │ 5af8977d22913560b64c0c2b6001f914d097146b │
╘════════════════════╧═════════╧═════════════════════════════════════╧══════════════════╧══════════════════════════════════════════╛

```


#### Workflow

#### Installing and deps
This project depends on python 3.7+ install
[python virtualenv](https://virtualenv.pypa.io/en/latest/).  

Prerequisites:

> python 3.7   
libgit2, libgit2-glib - needed for macbook and fedora.

```bash
$ virtualenv -p python3 .venv
....
# activate the virtualenv
source .venv/bin/activate
```

Now you can install the application

```bash
$: python3.7 setup.py install
```