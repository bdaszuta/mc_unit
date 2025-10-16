#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 ,-*
(_)

@author: Boris Daszuta
@function: Miscellanous functions that do not fit elsewhere.
"""
def _import_clear(name):
  to_del_cmd = "import sys as _sys\n"
  to_del_cmd += "if not hasattr(_sys, 'ps1'):\n"
  to_del_cmd += "  {name} = False\n"
  to_del_cmd += "del {name}"

  return to_del_cmd.format(name=name)

#
# :D
#
