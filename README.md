# mc_unit
Fast food, fast units.

## basic example:
```python
import mc_unit as mu

conv_gra = mu.conv_gra

rho_gra = 1e-12
rho_cgs = rho_gra * conv_gra["rho [g cm^-3]"].value
```

The `conv_gra` is a convenience variable that is assembled from fundamental specification. More specifically:

```python
conv_gra = {
  "rho [g cm^-3]": Constant(
    us_GeometricSolar(us_CGS, "density", 1) *
    us_GeometricSolar(us_CGS, "mass", 1),
    "gra_cu -> g cm^-3"
  ),
  # ...
}
```

## inter-system conversion:
```python
from mc_unit import (us_GeometricSolar, us_CGS, us_SI)

mu_gra = 10 # MeV

# result in "erg" - check unit with us_CGS()
mu_cgs = us_GeometricSolar(us_CGS, "chemical_potential", mu_gra)

# result in "J" - again, check unit with us_SI()
mu_SI = us_GeometricSolar(us_SI, "chemical_potential", mu_gra)

# start with a different system and go back
# More precisely this verifies the "transitive property"
mu_SI_r = us_CGS(us_SI, "chemical_potential", mu_cgs)
```

## additional info:
See `usage.py`.

Specification and conversion logic based on `PrimitiveSolver` ( https://github.com/jfields7/primitive-solver/ ).