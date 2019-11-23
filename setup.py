#!/usr/bin/env python3
from setuptools import find_packages, setup

setup(
    name='competitive-programming-ci-script',
    version='0.1.0',
    author='Kimiyuki Onaka',
    author_email='kimiyuki95@gmail.com',
    url='https://github.com/kmyk/competitive-programming-ci-script',
    license='MIT License',
    description='',
    install_requires=[
        'online-judge-tools == 7.*',
    ],
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        'console_scripts': [
            'oj-ci = onlinejudge_ci.main:main',
        ],
    },
)
