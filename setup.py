from setuptools import setup, find_packages

VERSION='0.1.0'

long_description="""
Hurd is a CI/CD tool for pinning microservices under a unified platform.
"""

packages=[
    'hurd',
]

install_requires=[
    'click',
    'pygit2',
    'pyyaml',
    'tabulate',
]

def main():
    setup_info = dict(
        name='hurd',
        version=VERSION,
        url="https://github.com/pi-victor/hurd",
        author='Victor Palade <victor@cloudflavor.io>',
        description='A microservice platform tool for CI/CD pipelines',
        long_description=long_description,
        license='Apache-2.0',
        packages=packages,
        install_requires=install_requires,
        zip_safe=False,
    )

    setup(**setup_info)

if __name__ == '__main__':
    main()
