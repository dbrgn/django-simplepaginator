#!/usr/bin/env python

from distutils.core import setup

setup(name='simple_paginator',
      version='0.1',
      description='A simple wrapper around the Django paginator',
      author='Factor AG',
      author_email='webmaster@factor.ch',
      url='https://github.com/FactorAG/django-simplepaginator',
      license='LGPLv3',
      packages=['simple_paginator', 'simple_paginator.templatetags'],
      package_dir={'messagegroups': 'messagegroups'},
      package_data={'simple_paginator': ['templates/*']},
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