#!/usr/bin/env python
# coding: UTF-8

from setuptools import setup, find_packages

setup(name='annofabapi',
      version='0.0.1',
      description='Python Clinet Library of AnnoFab API (https://annofab.com/docs/api/)',
      author='yuji38kwmt',
      license='MIT',
      keywords='annofab api',
      url='https://github.com/kurusugawa-computer/annofab-api-python-client',
      install_requires=['requests', 'python-dateutil', 'backoff'],
      classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3 :: Only",
            "Topic :: Utilities",
      ],
      packages=find_packages(exclude=["tests"])
      )
