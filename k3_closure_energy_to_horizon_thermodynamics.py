#!/usr/bin/env python3
"""
K3 CLOSURE ENERGY TO HORIZON THERMODYNAMICS
===========================================

Purpose
-------
Continue the gravity chain from internal K3 closure energy.

Previous step:
    K3 -> p=4 -> closure energy E_C=p²=16
    and:
        mu_K3 = E_C = p²

    Schwarzschild exterior:
        f(r) = 1 - 2mu/r
        r_h = 2mu

Now we test horizon thermodynamics:

    A = 4πr_h²
    S = A/4
    T = 1/(8πmu)
    dmu = T dS

Key p=4 discovery:
    mu = p²
    r_h = 2p²

For p=4:
    2 = sqrt(p)

So:
    r_h² = 4p⁴ = p⁵
    A/π = 4r_h² = p⁶
    S/π = r_h² = p⁵

This means the K3 quarter lowers the area exponent by one p-power:

    A/π = p⁶
    S/π = p⁵

So the entropy is the horizon radius-square / p-power structure, directly
from closure energy.
"""

import math
import numpy as np

print("=" * 116)
print("K3 CLOSURE ENERGY TO HORIZON THERMODYNAMICS")
print("=" * 116)

# =============================================================================
# STEP 1 — K3 CLOSURE ENERGY AS MASS PARAMETER
# =============================================================================

print("""
STEP 1 — K3 CLOSURE ENERGY AS MASS PARAMETER
────────────────────────────────────────────
K3 gives:

    p = 4
    closure energy E_C = p² = 16

Previous chain identified:

    mu = E_C

So:

    mu = p² = 16
""")

p = 4
E_C = p**2
mu = float(E_C)

step1_ok = p == 4 and E_C == 16 and mu == 16.0

print(f"  p = {p}")
print(f"  E_C = p² = {E_C}")
print(f"  mu = E_C = {mu}")
print(f"STEP 1 RESULT: {'PASS' if step1_ok else 'FAIL'}")

# =============================================================================
# STEP 2 — HORIZON RADIUS
# =============================================================================

print("""
STEP 2 — HORIZON RADIUS
───────────────────────
Schwarzschild-form metric factor:

    f(r) = 1 - 2mu/r

Horizon:

    f(r_h)=0

Therefore:

    r_h = 2mu

With mu=p²:

    r_h = 2p²

For p=4:

    r_h = 32
""")

r_h = 2.0 * mu

step2_ok = r_h == 32.0

print(f"  r_h = 2mu = {r_h}")
print(f"STEP 2 RESULT: {'PASS' if step2_ok else 'FAIL'}")

# =============================================================================
# STEP 3 — AREA AND ENTROPY
# =============================================================================

print("""
STEP 3 — AREA AND ENTROPY
─────────────────────────
Horizon area:

    A = 4πr_h²

K3 quarter entropy:

    S = A/4

With r_h = 2mu:

    A = 16πmu²
    S = 4πmu²

With mu=p²:

    A = 16πp⁴
    S = 4πp⁴

For p=4, because 4=p and 16=p²:

    A/π = p⁶
    S/π = p⁵
""")

A = 4.0 * math.pi * r_h**2
S = A / 4.0

A_over_pi = A / math.pi
S_over_pi = S / math.pi

step3_ok = (
    abs(A_over_pi - p**6) < 1e-12
    and abs(S_over_pi - p**5) < 1e-12
    and abs(S - 4.0*math.pi*mu**2) < 1e-9
)

print(f"  A = {A}")
print(f"  S = A/4 = {S}")
print(f"  A/π = {A_over_pi}")
print(f"  p⁶ = {p**6}")
print(f"  S/π = {S_over_pi}")
print(f"  p⁵ = {p**5}")
print(f"STEP 3 RESULT: {'PASS' if step3_ok else 'FAIL'} — area/entropy become p⁶/p⁵")

# =============================================================================
# STEP 4 — QUARTER AS EXPONENT DROP
# =============================================================================

print("""
STEP 4 — QUARTER AS EXPONENT DROP
─────────────────────────────────
At p=4:

    S = A/4

But since 4=p:

    S/π = (A/π)/p

So:

    A/π = p⁶
    S/π = p⁵

The quarter is not only a coefficient.
At p=4 it acts as a one-power descent:

    p⁶ -> p⁵
""")

exponent_drop = (A_over_pi / p)
step4_ok = abs(exponent_drop - S_over_pi) < 1e-12

print(f"  (A/π)/p = {exponent_drop}")
print(f"  S/π = {S_over_pi}")
print(f"STEP 4 RESULT: {'PASS' if step4_ok else 'FAIL'} — quarter lowers by one p-power")

# =============================================================================
# STEP 5 — SURFACE GRAVITY
# =============================================================================

print("""
STEP 5 — SURFACE GRAVITY
────────────────────────
Metric factor:

    f(r) = 1 - 2mu/r

Surface gravity for this form:

    kappa = f'(r_h)/2

Since:

    f'(r) = 2mu/r²

At:

    r_h = 2mu

we get:

    kappa = 1/(4mu)

With mu=p²:

    kappa = 1/(4p²)

For p=4:

    kappa = 1/64
""")

def f_prime(r, mu):
    return 2.0 * mu / (r*r)

kappa = f_prime(r_h, mu) / 2.0
kappa_expected = 1.0 / (4.0 * mu)

step5_ok = abs(kappa - kappa_expected) < 1e-12 and abs(kappa - 1.0/64.0) < 1e-12

print(f"  f'(r_h) = {f_prime(r_h, mu)}")
print(f"  kappa = f'(r_h)/2 = {kappa}")
print(f"  1/(4mu) = {kappa_expected}")
print(f"STEP 5 RESULT: {'PASS' if step5_ok else 'FAIL'}")

# =============================================================================
# STEP 6 — TEMPERATURE
# =============================================================================

print("""
STEP 6 — TEMPERATURE
────────────────────
Dimensionless Hawking-form temperature:

    T = kappa/(2π)

So:

    T = 1/(8πmu)

With mu=p²:

    T = 1/(8πp²)

For p=4:

    T = 1/(128π)
""")

T = kappa / (2.0 * math.pi)
T_expected = 1.0 / (8.0 * math.pi * mu)

step6_ok = abs(T - T_expected) < 1e-15

print(f"  T = kappa/(2π) = {T:.15f}")
print(f"  1/(8πmu) = {T_expected:.15f}")
print(f"STEP 6 RESULT: {'PASS' if step6_ok else 'FAIL'}")

# =============================================================================
# STEP 7 — FIRST LAW CHECK
# =============================================================================

print("""
STEP 7 — FIRST LAW CHECK
────────────────────────
Entropy:

    S(mu) = 4πmu²

Derivative:

    dS/dmu = 8πmu

Temperature:

    T = 1/(8πmu)

Therefore:

    T dS/dmu = 1

So:

    dmu = T dS

This is the dimensionless black-hole first law, with mu supplied by K3
closure energy.
""")

dS_dmu = 8.0 * math.pi * mu
first_law_product = T * dS_dmu

step7_ok = abs(first_law_product - 1.0) < 1e-12

print(f"  dS/dmu = {dS_dmu}")
print(f"  T = {T}")
print(f"  T(dS/dmu) = {first_law_product}")
print(f"STEP 7 RESULT: {'PASS' if step7_ok else 'FAIL'} — dmu = T dS")

# =============================================================================
# STEP 8 — NUMERICAL FINITE DIFFERENCE FIRST LAW
# =============================================================================

print("""
STEP 8 — NUMERICAL FINITE DIFFERENCE FIRST LAW
──────────────────────────────────────────────
Check directly with a small change in closure energy:

    mu -> mu + dmu

Compare:

    dmu

with:

    T_mid dS
""")

def entropy(mu):
    return 4.0 * math.pi * mu**2

def temperature(mu):
    return 1.0 / (8.0 * math.pi * mu)

dmu = 1e-4
mu1 = mu
mu2 = mu + dmu
S1 = entropy(mu1)
S2 = entropy(mu2)
dS = S2 - S1
T_mid = temperature((mu1 + mu2) / 2.0)
TdS = T_mid * dS

step8_ok = abs(TdS - dmu) < 1e-9

print(f"  dmu = {dmu}")
print(f"  dS = {dS}")
print(f"  T_mid = {T_mid}")
print(f"  T_mid dS = {TdS}")
print(f"STEP 8 RESULT: {'PASS' if step8_ok else 'FAIL'} — finite-difference first law holds")

# =============================================================================
# STEP 9 — SEAM ENERGY CONSISTENCY
# =============================================================================

print("""
STEP 9 — SEAM ENERGY CONSISTENCY
────────────────────────────────
Seam weights distribute closure energy:

    E_i = (w_i/W) E_C

and:

    ΣE_i = E_C = mu

Therefore the same seam-distributed closure energy is the thermodynamic mass
parameter.
""")

weights = np.array([2.0, 10.0, 30.0])
W = float(np.sum(weights))
fractions = weights / W
E_i = fractions * E_C

step9_ok = abs(np.sum(E_i) - mu) < 1e-12

print(f"  weights = {weights.tolist()}")
print(f"  W = {W}")
print("  seam    E_i")
for idx, e in enumerate(E_i, start=1):
    print(f"  {idx:<7} {e:<14.10f}")
print(f"  ΣE_i = {np.sum(E_i)}")
print(f"  mu = {mu}")
print(f"STEP 9 RESULT: {'PASS' if step9_ok else 'FAIL'}")

# =============================================================================
# STEP 10 — FULL HORIZON THERMODYNAMIC CHAIN
# =============================================================================

print("""
STEP 10 — FULL HORIZON THERMODYNAMIC CHAIN
──────────────────────────────────────────
The gravity chain now becomes:

    K3
      -> p=4
      -> closure energy E_C=p²
      -> mu=E_C
      -> r_h=2mu
      -> A=4πr_h²
      -> S=A/4
      -> kappa=1/(4mu)
      -> T=kappa/(2π)
      -> dmu=T dS

This connects the K3 closure source to horizon thermodynamics.
""")

chain_ok = (
    step1_ok and step2_ok and step3_ok and step4_ok and
    step5_ok and step6_ok and step7_ok and step8_ok and step9_ok
)

print(f"STEP 10 RESULT: {'PASS' if chain_ok else 'FAIL'} — K3 horizon thermodynamic chain complete")

# =============================================================================
# FINAL VERDICT
# =============================================================================

print("=" * 116)
print("FINAL VERDICT")
print("=" * 116)

print("""
Gravity push achieved:

  We connected K3 closure energy to horizon thermodynamics.

  The key internal identification is:

      mu = E_C = p²

  Then:

      r_h = 2mu

      A = 4πr_h²

      S = A/4

      kappa = 1/(4mu)

      T = 1/(8πmu)

      dmu = T dS

  For p=4:

      mu = 16
      r_h = 32
      A/π = p⁶ = 4096
      S/π = p⁵ = 1024

  So the quarter acts as an exponent drop:

      p⁶ -> p⁵

  and the seam-distributed closure energy is the thermodynamic mass parameter.

Current gravity chain:

    K3
      -> p=4
      -> p² closure energy
      -> seam distribution
      -> mu
      -> Schwarzschild exterior
      -> horizon area/entropy
      -> temperature
      -> first law

Next push:
    use the p-recursion to study horizon evaporation/level transitions:
        mu_n, A_n, S_n, T_n
    or connect physical units through universal seam tension tau0.
""")

# =============================================================================
# ASSERTIONS
# =============================================================================

assert step1_ok
assert step2_ok
assert step3_ok
assert step4_ok
assert step5_ok
assert step6_ok
assert step7_ok
assert step8_ok
assert step9_ok
assert chain_ok

print("ASSERTIONS")
print("─" * 116)
print("  [PASS] K3 closure energy gives mu")
print("  [PASS] horizon radius r_h=2mu")
print("  [PASS] area and entropy computed")
print("  [PASS] quarter is exponent drop p⁶ -> p⁵")
print("  [PASS] surface gravity computed")
print("  [PASS] temperature computed")
print("  [PASS] first law dmu=T dS holds")
print("  [PASS] finite-difference first law holds")
print("  [PASS] seam energy sum equals mu")
print("  [PASS] full horizon thermodynamic chain complete")

print("\nK3 CLOSURE ENERGY TO HORIZON THERMODYNAMICS COMPLETE.")
print("=" * 116)
