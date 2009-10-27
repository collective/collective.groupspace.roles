# -*- coding: utf-8 -*-
"""
groupspace.roles
"""

import os

from setuptools import find_packages
from setuptools import setup

__version__ = '1.0'

__here__ = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(__here__, 'README.txt')).read()
CHANGES = open(os.path.join(__here__, 'CHANGES.txt')).read()

setup(name='groupspace.roles',
    version=__version__,
    description="A roles tab for assigning dynamic local roles",
    long_description=README + '\n\n' +  CHANGES,
    classifiers=[
      "Development Status :: 4 - Beta",
      "Environment :: Web Environment",
      "Framework :: Plone",
      "Framework :: Zope2",
      "License :: OSI Approved :: GNU General Public License (GPL)",
      "Operating System :: OS Independent",
      "Programming Language :: Python",
      "Topic :: Communications :: Email",
      "Topic :: Internet :: WWW/HTTP :: Dynamic Content",        
      "Topic :: Office/Business :: Groupware",
      "Topic :: Software Development :: Libraries :: Python Modules",
      ],
    keywords='GrufSpaces, GroupSpace, Roles, PAS, borg.localrole',
    author='Maik Röder',
    author_email='roeder@berg.net',
    url='https://svn.plone.org/svn/collective/groupspace.roles',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['groupspace'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
    ],
    entry_points="""
    # -*- Entry points: -*-

    [distutils.setup_keywords]
    paster_plugins = setuptools.dist:assert_string_list

    [egg_info.writers]
    paster_plugins.txt = setuptools.command.egg_info:write_arg
    """,
    paster_plugins = ["ZopeSkel"],
    )
