#!/usr/bin/env python
# coding: UTF-8

from setuptools import setup, find_packages
import os

setup(name='annofabapi',
      version='0.2.0',
      description='Annofab API（https://annofab.com/api/v1/）にアクセスするライブラリです。',
      author='yuji38kwmt',
      url='https://github.com/kurusugawa-computer/annofab-api-access-python-commons',
      install_requires=['requests', 'backoff'],
      packages=find_packages(exclude=["tests"])
      )
