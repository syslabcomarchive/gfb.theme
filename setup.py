from setuptools import setup, find_packages

version = '0.1'

setup(name='gfb.theme',
      version=version,
      description="An installable theme for Plone 3.0",
      long_description="""\
This Skin is used for the german GFB project""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone skin gfb',
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
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
