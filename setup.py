# -*- coding: utf-8 -*-
"""
This module contains the gfb.theme package
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.3.13dev'

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('gfb', 'theme', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' 
    )
    
tests_require=['zope.testing']
setup(name='gfb.theme',
      version=version,
      description="An installable theme for Plone 3.0",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone skin gfb baua',
      author='Syslab.com GmbH',
      author_email='info@syslab.com',
      url='https://svn.syslab.com/svn/syslabcom/gfb',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['gfb'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'collective.dynatree',
          'z3c.json',
          'Products.AdvancedQuery',
          'Products.ATVocabularyManager',
          'Products.CMFCore',
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'gfb.theme.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*- 
      """,
      )      
      
