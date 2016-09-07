#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

_theconfig = None

BASE_DIRECTORY = None


def base_directory():
    return BASE_DIRECTORY
