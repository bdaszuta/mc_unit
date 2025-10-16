"""
 ,-*
(_)

@author: Boris Daszuta
@function: Gather defined unit-systems
"""
from .units import (
  us_CGS,
  us_SI,
  us_GeometricKilometer,
  us_GeometricSolar,
  us_Nuclear,
)

from .code_conventions import (
  conv_gra
)

# reduce import spam in interpreter: compat with pytest -----------------------
# pylint: disable=exec-used
from .miscellaneous import (_import_clear, )
exec(_import_clear("miscellaneous"))
exec(_import_clear("code_conventions"))
exec(_import_clear("units"))
# =============================================================================

#
# :D
#
