#!/usr/bin/env python3

# Copyright 2016 Science & Technology Facilities Council
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from subprocess import check_output
from distutils.core import setup

def get_version():
    """Returns a version for the package, based on git-describe"""
    return check_output("git describe --always".split()).decode().strip()

setup(
    name='markdown-spellchecker',
    version=get_version(),
    description='markdown-spellchecker',
    long_description='''Spellchecker for documentation written with markdown''',
    license='Apache 2.0',
    author='Science & Technology Facilities Council',
    author_email='enquiries@stfc.ac.uk',
    py_modules=['markspelling'],
    data_files=[('/etc/markdown-spellchecker/', ['src/config.ini'])],
    scripts=['src/spellchecker.py'],
    url='http://www.scd.stfc.ac.uk/'
)
