#!/usr/bin/env python
# coding: UTF-8

from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(name='annofabapi',
      version='0.1.2',
      description=
      'Python Clinet Library of AnnoFab API (https://annofab.com/docs/api/)',
      long_description=readme,
      long_description_content_type='text/markdown',
      author='yuji38kwmt',
      author_email='yuji38kwmt@gmail.com',
      maintainer='yuji38kwmt',
      license='MIT',
      keywords='annofab api',
      url='https://github.com/kurusugawa-computer/annofab-api-python-client',
      install_requires=['requests', 'python-dateutil', 'backoff'],
      python_requires='>=3.6',
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3 :: Only",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Topic :: Utilities",
      ],
      packages=['annofabapi'])
