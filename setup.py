#!/usr/bin/env python3
from setuptools import find_packages, setup

setup(
    name='online-judge-verify-helper',
    version='4.8.0',
    author='Kimiyuki Onaka',
    author_email='kimiyuki95@gmail.com',
    url='https://github.com/kmyk/online-judge-verify-helper',
    license='MIT License',
    description='',
    python_requires='>=3.6',
    install_requires=[
        'pyyaml',
        'online-judge-tools >= 8.0.0',
        'setuptools',
        'toml',
    ],
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={
        'onlinejudge_verify_resources': ['*', 'assets/*', 'assets/css/*', 'assets/js/*'],
    },
    entry_points={
        'console_scripts': [
            'oj-verify = onlinejudge_verify.main:main',
            'oj-bundle = onlinejudge_bundle.main:main',
        ],
    },
)
