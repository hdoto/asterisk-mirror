# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# production
requires = ['rpi.gpio']
# development
#requires = ['fake_rpi', 'pylint']
entries = {
    'console_scripts': [
        'asterisk_mirror = asterisk_mirror.main:main'
    ]
}

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='asterisk-mirror',
    version='1.0.0',
    description='Asterisk Mirror',
    long_description=readme,
    author='Junichi Yura',
    author_email='yurayura@gmail.com',
    url='http://www.howeb.org',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=requires,
    entry_points=entries
)
