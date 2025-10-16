#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 ,-*
(_)

@author: Boris Daszuta
@function: Common stuffs.
"""
from dataclasses import dataclass

import numpy as np

@dataclass(frozen=True)
class Constant:
  value: float
  unit: str

  # overload unary operations
  def __neg__(self):
    return Constant(-self.value, self.unit)

  def __pos__(self):
    return Constant(+self.value, self.unit)

  def __abs__(self):
    return Constant(abs(self.value), self.unit)

  # overload binary operations
  def __add__(self, other):
    if isinstance(other, Constant):
      return Constant(self.value + other.value, self.unit)
    return Constant(self.value + other, self.unit)

  def __radd__(self, other):
    return self.__add__(other)

  def __sub__(self, other):
    if isinstance(other, Constant):
      return Constant(self.value - other.value, self.unit)
    return Constant(self.value - other, self.unit)

  def __rsub__(self, other):
    if isinstance(other, Constant):
      return Constant(other.value - self.value, self.unit)
    return Constant(other - self.value, self.unit)

  def __mul__(self, other):
    if isinstance(other, Constant):
      return Constant(self.value * other.value, self.unit)
    return Constant(self.value * other, self.unit)

  def __rmul__(self, other):
    return self.__mul__(other)

  def __truediv__(self, other):
    if isinstance(other, Constant):
      return Constant(self.value / other.value, self.unit)
    return Constant(self.value / other, self.unit)

  def __rtruediv__(self, other):
    if isinstance(other, Constant):
      return Constant(other.value / self.value, self.unit)
    return Constant(other / self.value, self.unit)

  def __pow__(self, exponent):
    return Constant(self.value ** exponent, self.unit)

def POWN(x, n):
  return np.power(x, n)

def POW2(x):
  return x * x

def POW3(x):
  return x * x * x

def POW4(x):
  return POW2(x) * POW2(x)

#
# :D
#
