# ===============================================================================
# Copyright 2017 dgketchum
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

import os

from setuptools import setup

os.environ['TRAVIS_CI'] = 'True'

try:
    from setuptools import setup

    setup_kwargs = {'entry_points': {'console_scripts': ['landsat_dl=landsat_dl.cli:cli']}}
except ImportError:
    from distutils.core import setup

    setup_kwargs = {'scripts': ['bin/landsat_dl/cli']}

with open('README.md') as f:
    readme = f.read()

tag = '0.13.0'

setup(name='landsat_dl',
      version=tag,
      description='Very simple API to download Landsat data from Landsat 1 - 5, 7, and 8 from Google',
      long_description=readme,
      setup_requires=['nose>=1.0'],
      py_modules=['landsat_dl'],
      license='Apache',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: GIS',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6'],
      keywords='landsat download hydrology remote sensing',
      author='Lei Guo',
      author_email='tristanblus@csu.edu.cn',
      platforms='Posix; MacOS X; Windows',
      packages=['landsat_dl'],
      download_url='https://github.com/{}/{}/archive/{}.tar.gz'.format('tristanblus', 'landsat_dl', tag),
      url='https://github.com/tristanblus',
      test_suite='tests.test_suite.suite',
      install_requires=['requests', 'tqdm', 'click', 'shapely', 'python-dateutil', 'pretty_errors'],
      **setup_kwargs)


# ============= EOF ==============================================================
