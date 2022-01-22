# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='farmers_world_automation_script',
    version='0.0.1',
    description='Automated operation script for the Farmers  World.',
    long_description=readme,
    author='biaowong',
    author_email='biaowong@tutanota.com',
    url='https://github.com/biaowong/farmers-world-automation-script',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)