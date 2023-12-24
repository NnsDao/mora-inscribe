#!/usr/bin/env python

import os
# import sys
# import environ
# from pathlib import Path




def get_root():
    return os.path.dirname(os.path.abspath(__file__))

def ic_app_path():
    return os.path.join(get_root(), 'ic_app')

def mora_inscribe_path():
    return os.path.join(get_root(), 'mora_inscribe')



