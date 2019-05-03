#!/usr/bin/env python
# coding: UTF-8

from setuptools import setup, find_packages

setup(name='annofabapi',
      version='0.0.1',
      description='Annofab API（https://annofab.com/api/v1/）にアクセスするライブラリです。',
      author='yuji38kwmt',
      url='https://github.com/kurusugawa-computer/annofab-api-python-client',
      install_requires=['requests', 'backoff'],
      packages=find_packages(exclude=["tests"])
      )
