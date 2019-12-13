#!/usr/bin/env python3
from setuptools import find_packages, setup

setup(
    name='online-judge-verify-helper',
    version='2.5.0',
    author='Kimiyuki Onaka',
    author_email='kimiyuki95@gmail.com',
    url='https://github.com/kmyk/online-judge-verify-helper',
    license='MIT License',
    description='',
    install_requires=[
        'markdown',
        'pyyaml',
        'online-judge-tools >= 7.4.*',
        'setuptools',
    ],
    packages=find_packages(exclude=('tests', 'docs')) + ['onlinejudge_verify.data'],
    package_dir={
        'onlinejudge_verify.data': 'data',
    },
    package_data={
        'onlinejudge_verify.data': ['*', 'assets/*', 'assets/css/*', 'assets/js/*'],
    },
    entry_points={
        'console_scripts': [
            'oj-verify = onlinejudge_verify.main:main',
        ],
    },
)
