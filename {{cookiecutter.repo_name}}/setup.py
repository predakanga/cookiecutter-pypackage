#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

try:
    from setuptools.command.test import test as TestCommand
    class Tox(TestCommand):
        def finalize_options(self):
            TestCommand.finalize_options(self)
            self.test_args = []
            self.test_suite = True
        def run_tests(self):
            #import here, cause outside the eggs aren't loaded
            import tox
            errcode = tox.cmdline(self.test_args)
            sys.exit(errcode)
except ImportError:
    Tox = None

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

# Extract our requirements
try:
    from pip.req import parse_requirements
    pip_reqs = parse_requirements('requirements.txt')
    requirements = [str(r.req) for r in pip_reqs]
except ImportError:
    with open('requirements.txt') as f:
        requirements = filter(lambda line: not line.startswith("#") and not line.startswith("-") and len(line),
                              f.read().splitlines())

setup(
    name='{{ cookiecutter.repo_name }}',
    version='{{ cookiecutter.version }}',
    description='{{ cookiecutter.project_short_description }}',
    long_description=readme + '\n\n' + history,
    author='{{ cookiecutter.full_name }}',
    author_email='{{ cookiecutter.email }}',
    url='https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}',
    packages=[
        '{{ cookiecutter.repo_name }}',
    ],
    package_dir={'{{ cookiecutter.repo_name }}': '{{ cookiecutter.repo_name }}'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='{{ cookiecutter.repo_name }}',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
    test_requires=['tox'],
    cmdclass = {'test': Tox},
)
