import os
import sys
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'gevent-spider',
    version = '0.1',
    description = 'A simple spider with a realtime web-based frontend.',
    long_description = read('README.rst'),
    url = 'http://github.com/codysoyland/gevent-spider/',
    license = 'BSD',
    author = 'Cody Soyland',
    author_email = 'cody@soyland.com',
    packages = find_packages(exclude=['tests']),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires = ['gevent', 'gevent-websocket', 'lxml', 'requests'],

    tests_require = ['nose'],
    test_suite = 'nose.collector',

    entry_points = {
        'console_scripts': ['gevent-spider-web = gevent_spider.cli:web']
    }
)
