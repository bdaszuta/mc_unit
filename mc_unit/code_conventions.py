#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 ,-*
(_)

@author: Boris Daszuta
@function: Conversions for various codes.
"""
import numpy as np

from .common import Constant
from .units import (us_CGS, us_GeometricSolar, us_Nuclear, us_SI)

# conversion factors from code units of GR-Athena++ to common physical units
conv_gra = {
  "mass [g]": Constant(
    us_GeometricSolar(us_CGS, "mass", 1),
    "gra_cu -> g"
  ),
  "rho [g cm^-3]": Constant(
    us_GeometricSolar(us_CGS, "density", 1) *
    us_GeometricSolar(us_CGS, "mass", 1),
    "gra_cu -> g cm^-3"
  ),
  "n [cm^-3]": Constant(
    us_GeometricSolar(us_CGS, "density", 1),
    "gra_cu -> cm^-3"
  ),
  "t [ms]": Constant(
    1000 * us_GeometricSolar(us_CGS, "time", 1),
    "gra_cu -> ms"
  ),
  "T [MeV]": Constant(
    1, # gra temperature always in MeV
    "gra_cu -> MeV"
  ),
  "T [GK]": Constant(
    us_Nuclear(us_SI, "temperature", 1) / 1e9,
    "gra_cu -> GK"
  ),
  "u [erg cm^-3]": Constant(
    us_GeometricSolar(us_CGS, "energy", 1) /
    us_GeometricSolar(us_CGS, "length", 1) ** 3,
    "gra_cu -> erg cm^-3"
  ),
  "l [km]": Constant(
    us_GeometricSolar(us_CGS, "length", 1) / 100 / 1000,
    "gra_cu -> km"
  ),
  "E [MeV]": Constant(
    us_GeometricSolar(us_Nuclear, "energy", 1),
    "gra_cu -> MeV"
  ),
  "L [erg s^-1]": Constant(
    us_GeometricSolar(us_CGS, "energy", 1) /
    us_GeometricSolar(us_CGS, "time", 1),
    "gra_cu -> erg s^-1"
  ),
  "B [G]": Constant(
    np.sqrt(4 * np.pi) *
    np.sqrt(us_GeometricSolar(us_CGS, "mass", 1) /
            us_GeometricSolar(us_CGS, "length", 1)) /
    us_GeometricSolar(us_CGS, "time", 1),
    "gra_cu -> G = cm^-1/2 g^1/2 s * (4 * pi)^1/2"
  )
}

#
# :D
#
