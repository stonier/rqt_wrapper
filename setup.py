#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['rqt_wrapper'],
    package_dir={'': 'src'},
    #scripts=['scripts/rqt_remocon' ],
    #scripts=['scripts/rocon_remocon','scripts/rqt_remocon' ],
)
setup(**d)
