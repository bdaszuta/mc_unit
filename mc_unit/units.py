#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 ,-*
(_)

@author: Boris Daszuta
@function: Define unit systems and conversions.
"""
import numpy as np
from .common import (
  POW2, POW3, POW4, Constant
)

class UnitSystem:
  """Base unit system class with universal, type-preserving direct-call conversion."""

  # Conversion ratio methods (src = self; for conversion clarity)
  def conv_length(src, tar):
    return tar.length.value / src.length.value

  def conv_time(src, tar):
    return tar.time.value / src.time.value

  def conv_velocity(src, tar):
    return (tar.length.value / src.length.value *
            src.time.value / tar.time.value)

  def conv_density(src, tar):
    return tar.density.value / src.density.value

  def conv_mass(src, tar):
    return tar.mass.value / src.mass.value

  def conv_energy(src, tar):
    return tar.energy.value / src.energy.value

  def conv_entropy(src, tar):
    return tar.kb.value / src.kb.value

  def conv_pressure(src, tar):
    return tar.pressure.value / src.pressure.value

  def conv_temperature(src, tar):
    return tar.temperature.value / src.temperature.value

  def conv_chemical_potential(src, tar):
    return (tar.chemical_potential.value /
            src.chemical_potential.value)

  # Direct-call universal converter
  def __call__(self, target_system=None, quantity=None, value=None):
    """
    Convert a value or array from this unit system to a target unit system.

    Usage:
    - source_system(target_system, "pressure", X)
    - source_system(target_system, "length", np.array([...]))

    If target_system is None, return internal factors.

    If quantity is None, returns a ConversionProxy for attribute-style usage.
    """
    if target_system is None:
      return {
        name: getattr(self, name) for name in [
          "c", "G", "kb", "Msun", "MeV",
          "length", "time", "density", "mass", "energy",
          "pressure", "temperature", "chemical_potential"
        ]
      }

    if quantity is None:
      return ConversionProxy(self, target_system)

    # Map quantity to conversion method
    quantity_map = {
      'length': self.conv_length,
      'time': self.conv_time,
      'velocity': self.conv_velocity,
      'density': self.conv_density,
      'mass': self.conv_mass,
      'energy': self.conv_energy,
      'entropy': self.conv_entropy,
      'pressure': self.conv_pressure,
      'temperature': self.conv_temperature,
      'chemical_potential': self.conv_chemical_potential
    }

    if quantity not in quantity_map:
      raise ValueError(f"Unknown quantity '{quantity}'")

    if value is None:
      raise ValueError("Must provide a value to convert")

    factor = quantity_map[quantity](target_system)

    # Apply factor and preserve input type
    if isinstance(value, np.ndarray):
      return value * factor
    elif isinstance(value, (list, tuple)):
      return type(value)(v * factor for v in value)
    else:  # scalar
      return value * factor


class ConversionProxy:
  """Proxy for attribute-style conversion: src_us(tar_us).quantity(value)"""
  def __init__(self, source_unit, target_unit):

    if not isinstance(source_unit, UnitSystem):
      raise ValueError("source_unit must be a UnitSystem")

    if not isinstance(target_unit, UnitSystem):
      raise ValueError("target_unit must be a UnitSystem")

    self.source_unit = source_unit
    self.target_unit = target_unit

  def __getattr__(self, quantity):
    def converter(value):
      return self.source_unit(self.target_unit, quantity, value)
    return converter


# define specific unit systems ------------------------------------------------

class CGS(UnitSystem):
  # CGS units:
  #   Fundamental constants are defined using the 2014
  #   CODATA values to be consistent with CompOSE. Solar
  #   mass is derived from the solar mass parameter given
  #   in the 2021 Astronomer's Almanac:
  #   GM_S = 1.32712442099e26 cm^3 s^-2
  def __init__(self):

    # define physical constants -----------------------------------------------
    self.c = Constant(2.99792458e10, "cm s^-1")
    self.G = Constant(6.67408e-8, "cm^3 g^-1 s^-2")
    self.kb = Constant(1.38064852e-16, "erg K^-1")
    self.Msun = Constant(1.98848e33, "g")
    self.MeV = Constant(1.6021766208e-6, "erg")

    # conversion rules --------------------------------------------------------
    self.length = Constant(1.0, "cm")
    self.time = Constant(1.0, "s")
    self.density = Constant(1.0, "g cm^-3")
    self.mass = Constant(1.0, "g")
    self.energy = Constant(1.0, "erg")
    self.pressure = Constant(1.0, "erg cm^-3")
    self.temperature = Constant(1.0, "K")
    self.chemical_potential = Constant(1.0, "erg")

class SI(UnitSystem):
  # International System of Units (SI)
  def __init__(self):
    cgs = CGS()

    # define physical constants -----------------------------------------------
    self.c = Constant(
      cgs.c.value / 100,  # cm -> m
      "m s^-1"
    )
    self.G = Constant(
      cgs.G.value * POW3(1 / 100) / (1 / 1000), # cm^3 g^-1 -> m^3 kg^-1
      "m^3 kg^-1 s^-2"
    )
    self.kb = Constant(
      cgs.kb.value * 1e-7, # erg -> J
      "J K^-1"
    )
    self.Msun = Constant(
      cgs.Msun.value / 1000, # g -> kg
      "kg"
    )
    self.MeV = Constant(
      cgs.MeV.value * 1e-7, # erg -> J
      "J"
    )

    # conversion rules --------------------------------------------------------
    self.length = Constant(
      0.01,
      "m"     # 1 cm = 1e-2 m
    )
    self.time = Constant(
      1.0,
      "s"
    )
    self.density = Constant(
      1000.0,
      "kg m^-3" # 1 g cm^-3 = 1000 kg m^-3
    )
    self.mass = Constant(
      0.001,
      "kg"    # 1 g = 1e-3 kg
    )
    self.energy = Constant(
      1.0e-7,
      "J"     # 1 erg = 1e-7 J
    )
    self.pressure = Constant(
      0.1,
      "Pa"    # 1 erg cm^-3 = 0.1 Pa
    )
    self.temperature = Constant(
      1.0,
      "K"
    )
    self.chemical_potential = Constant(
      1.0e-7,
      "J"     # same conversion as energy
    )

class GeometricKilometer(UnitSystem):
  # Geometric units with length in kilometers
  def __init__(self):
    cgs = CGS()

    # define physical constants -----------------------------------------------
    self.c = Constant(1.0, "-")
    self.G = Constant(1.0, "-")
    self.kb = Constant(1.0, "-")
    self.Msun = Constant(
      cgs.Msun.value * cgs.G.value / POW2(cgs.c.value) * 1e-5,
      "km"
    )
    self.MeV = Constant(
      cgs.MeV.value * cgs.G.value / POW4(cgs.c.value) * 1e-5,
      "km"
    )

    # conversion rules --------------------------------------------------------
    self.length = Constant(1e-5,
      "km"
    )
    self.time = Constant(
      cgs.c.value * 1e-5,
      "km"
    )
    self.density = Constant(1e15,
      "km^-3"
    )
    self.mass = Constant(
      cgs.G.value / POW2(cgs.c.value) * 1e-5,
      "km"
    )
    self.energy = Constant(
      cgs.G.value / POW4(cgs.c.value) * 1e-5,
      "km"
    )
    self.pressure = Constant(
      cgs.G.value / POW4(cgs.c.value) * 1e10,
      "km^-2"
    )
    self.temperature = Constant(
      cgs.kb.value * cgs.G.value / POW4(cgs.c.value) * 1e-5,
      "km"
    )
    self.chemical_potential = Constant(
      cgs.kb.value / cgs.MeV.value,
      "MeV"
    )

class GeometricSolar(UnitSystem):
  # Geometric units with length in solar masses
  def __init__(self):
    cgs = CGS()

    # define physical constants -----------------------------------------------
    self.c = Constant(1.0, "-")
    self.G = Constant(1.0, "-")
    self.kb = Constant(1.0, "-")
    self.Msun = Constant(1.0, "-")
    self.MeV = Constant(
      cgs.MeV.value / POW2(cgs.c.value),
      "Msun"
    )

    # conversion rules --------------------------------------------------------
    self.length = Constant(
      POW2(cgs.c.value) / (cgs.G.value * cgs.Msun.value),
      "Msun"
    )
    self.time = Constant(
      POW3(cgs.c.value) / (cgs.G.value * cgs.Msun.value),
      "Msun"
    )
    self.density = Constant(
      POW3((cgs.G.value * cgs.Msun.value) / POW2(cgs.c.value)),
      "Msun^-3"
    )
    self.mass = Constant(
      1.0 / cgs.Msun.value,
      "Msun"
    )
    self.energy = Constant(
      1.0 / (cgs.Msun.value * POW2(cgs.c.value)),
      "Msun"
    )
    self.pressure = Constant(
      POW3(cgs.G.value / POW2(cgs.c.value)) *
      POW2(cgs.Msun.value / cgs.c.value),
      "Msun^-2"
    )
    self.temperature = Constant(
      cgs.kb.value / cgs.MeV.value,
      "MeV"
    )
    self.chemical_potential = Constant(
      cgs.kb.value / cgs.MeV.value,
      "MeV"
    )

class Nuclear(UnitSystem):
  # Nuclear units
  def __init__(self):
    cgs = CGS()

    # define physical constants -----------------------------------------------
    self.c = Constant(1.0, "-")
    self.G = Constant(
      cgs.G.value * cgs.MeV.value / POW4(cgs.c.value) * 1e13,
      "fm"
    )
    self.kb = Constant(1.0, "-")
    self.Msun = Constant(
      cgs.Msun.value * POW2(cgs.c.value) / cgs.MeV.value,
      "MeV"
    )
    self.MeV = Constant(1.0, "MeV")

    # conversion rules --------------------------------------------------------
    self.length = Constant(
      1e13,
      "fm"
    )
    self.time = Constant(
      cgs.c.value * 1e13,
      "fm"
    )
    self.density = Constant(
      1e-39,
      "fm^-3"
    )
    self.mass = Constant(
      POW2(cgs.c.value) / cgs.MeV.value,
      "MeV"
    )
    self.energy = Constant(
      1.0 / cgs.MeV.value,
      "MeV"
    )
    self.pressure = Constant(
      1e-39 / cgs.MeV.value,
      "MeV fm^-3"
    )
    self.temperature = Constant(
      cgs.kb.value / cgs.MeV.value,
      "MeV"
    )
    self.chemical_potential = Constant(
      cgs.kb.value / cgs.MeV.value,
      "MeV"
    )


# instantiate unit systems for ease of use ------------------------------------
us_CGS = CGS()
us_SI = SI()
us_GeometricKilometer = GeometricKilometer()
us_GeometricSolar = GeometricSolar()
us_Nuclear = Nuclear()

#
# :D
#
