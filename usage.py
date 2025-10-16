#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 ,-*
(_)

@author: Boris Daszuta
@function: Show usage of `mc_unit`

Conversion defined for:
  'length'
  'time'
  'velocity'
  'density'               N.B this should be considered a number density
  'mass'
  'energy'
  'entropy'
  'pressure'
  'temperature'
  'chemical_potential'
"""
###############################################################################
# python imports
import numpy as np

# package imports
from mc_unit import (us_CGS, us_SI, us_GeometricKilometer,
                     us_GeometricSolar, us_Nuclear)

# code specific conversions
from mc_unit import (conv_gra, )
###############################################################################

###############################################################################
# basic conversion:
###############################################################################

# single value
len_CGS = 1e5
len_geom_km = us_CGS(us_GeometricKilometer, "length", len_CGS)

# iterable
lens_CGS = (1e5, 2.2e3)
lens_CGS = np.array([1e5, 2.2e3])
lens_GK = us_CGS(us_GeometricKilometer, "length", lens_CGS)

# or via conversion proxy and attributes:
# lens_prox = us_CGS(us_GeometricKilometer).length
# lens_prox(lens_CGS)

# extract factors from the systems
# us_CGS()
# us_SI()
# us_GeometricKilometer()
# us_GeometricSolar()
# us_Nuclear()

###############################################################################
# converting [code_unit] out of GeometricSolar, as follows:
###############################################################################
print("GR-Athena++ unit conversions:")
for key, conv_info in conv_gra.items():
  print(f"{key}:", conv_info)

# so supposing we have rho=1e-12 in code units we can convert to g cm^-3 as:
rho_gra = 1e-12
rho_cgs = rho_gra * conv_gra["rho [g cm^-3]"]
print(f"rho_gra: {rho_gra}; rho_cgs: {rho_cgs}")

#
# :D
#
