#!/usr/bin/env python

from setuptools import setup, find_packages
from rabbit_dump import VERSION

url="https://www.google.com.hk/"

long_description="rabbit dump Python client"

setup(name="rabbit_dump",
      version=VERSION,
      description=long_description,
      maintainer="msheng",
      maintainer_email="msheng.ye@foxmail.com",
      url = url,
      long_description=long_description,
      install_requires = ['pika'],
      packages=find_packages('.'),
     )