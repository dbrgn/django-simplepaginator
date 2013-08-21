#!/usr/bin/env python

from setuptools import setup

setup(name='simple_paginator',
      version='0.3.0',
      description='A simple wrapper around the Django paginator',
      author='Factor AG',
      author_email='webmaster@factor.ch',
      maintainer='Danilo Bargen',
      maintainer_email='gezuru@gmail.com',
      url='https://github.com/dbrgn/django-simplepaginator',
      license='LGPLv3',
      keywords='django simple pagination paginator',
      packages=['simple_paginator'],
      platforms=['any'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Software Development :: Libraries :: Python Modules',
          ],
    )
