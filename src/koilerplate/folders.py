#!/usr/bin/env python

"""
This is the basic folder configurations for a Kaggle notebook. We define constants
that are the base folders for input, temp, and working paths in an OS agnostic way
which means that the notebook code works both in Kaggle and on a local PC.
"""

from __future__ import annotations

__author__ = "Andrew Scholan"
__credits__ = []
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Andrew Scholan"
__email__ = "andrew.scholan@scholan.com"
__status__ = "Development"

import os

INPUT_ROOT = os.path.abspath(os.path.join("..", "input"))
TEMP_ROOT = os.path.abspath(os.path.join("..", "temp"))
WORKING_ROOT = os.path.abspath(".")
