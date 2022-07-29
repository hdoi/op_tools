# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

setup(
    name='op_tools',
    version='0.2.1',
    description='op_tools',
    long_description=readme,
    author='Hideo Doi',
    author_email='doi.hideo.chemistry@gmail.com',
    url='https://github.com/hdoi/op_tools',
    license=license,
    install_requires=['numpy', 'scipy', 'pyquaternion', 'sympy', 'matplotlib'],
    packages=find_packages(exclude=('tests', 'docs'))
)
