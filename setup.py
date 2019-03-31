
# =========================================
#       IMPORTS
# --------------------------------------

import os
import setuptools
import setupextras

# DISABLED/BUG: this line fails when `pip install mybad` but works `pip install .`
# from mybad import __version__


# =========================================
#       MAIN
# --------------------------------------

name = 'mybad'
version = '0.1.4'
description = 'My friendly error base class - for Python.'
keywords = [
    'error',
    'errors',
    'baseclass',
    'meta',
    'debug',
    'inspector',
    'pretty',
    'color',
    'colors',
    'detailed',
    'stacktrace',
]

packages = setupextras.get_packages()
data_files = setupextras.get_data_files(['*.*'], os.path.join(name, 'tests', '__fixtures__'))
requirements = setupextras.get_requirements()
readme = setupextras.get_readme()

config = {
    'name': name,
    'version': version,
    'description': (description),
    'keywords': keywords,
    'author': 'Jonas Grimfelt',
    'author_email': 'grimen@gmail.com',
    'url': 'https://github.com/grimen/python-{name}'.format(name = name),
    'download_url': 'https://github.com/grimen/python-{name}'.format(name = name),
    'project_urls': {
        'repository': 'https://github.com/grimen/python-{name}'.format(name = name),
        'bugs': 'https://github.com/grimen/python-{name}/issues'.format(name = name),
    },
    'license': 'MIT',

    'long_description': readme,
    'long_description_content_type': 'text/markdown',

    'classifiers': [
        'Topic :: Software Development :: Libraries',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    'packages': packages,
    'package_dir': {
        name: name,
    },
    'package_data': {
        '': [
            'MIT-LICENSE',
            'README.md',
        ],
        name: [
            '*.*',
        ],
    },
    'data_files': data_files,
    'include_package_data': True,
    'zip_safe': True,

    'install_requires': requirements,
    'setup_requires': [
        'setuptools_git >= 1.2',
    ],
}

setuptools.setup(**config)
