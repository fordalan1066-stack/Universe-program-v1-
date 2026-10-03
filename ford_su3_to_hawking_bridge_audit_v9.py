#!/usr/bin/env python3
"""
FORD SU(3) -> HAWKING BRIDGE AUDIT
=================================
Version: v9
Date: 2026-08-15

PURPOSE
-------
Refine the previous uniqueness audit by separating:

1. identities forced directly by the SU(3) stiffness spectrum itself;
2. identities forced by standard ideal Hawking physics;
3. the ONE remaining physical bridge that still has to be justified.

KEY UPGRADE
-----------
The previous v8 presentation treated

    b^2 = 64
    b^3 c = 5120

as declared Hawking-mapping rules.

But once the SU(3) spectrum is written as

    (Gamma1^2, Gamma2^2, Gamma3^2) = s(a,b,c)

with

    s = gcd(24,64,80) = 8
    (a,b,c) = (3,8,10),

the middle primitive entry equals the common scale:

    s = b = 8.

Therefore

    Gamma2^2 = s*b = b^2 = 64

and

    Gamma3^2 = s*c = b*c = 80.

Hence

    Gamma2^2 * Gamma3^2
      = b^2 * b*c
      = b^3*c
      = 64*80
      = 5120.

So 5120 is already an internal algebraic consequence of the SU(3) stiffness
spectrum and its primitive decomposition.

The remaining issue is NOT the arithmetic identity. It is the physical theorem:

    Why must black-hole lifetime be proportional to
        (Fold-3 closure budget) x (Fold-2 inverse leakage time/rate)?

That is the bridge to prove.

STATUS LABELS
-------------
EXACT ALGEBRA:
    direct matrix or integer identity.

INTERNAL STRUCTURAL CONSEQUENCE:
    follows from the Ford fold spectrum with no Hawking input.

STANDARD HAWKING:
    follows from ordinary ideal Schwarzschild Hawking derivation.

OPEN PHYSICAL BRIDGE:
    needs a dynamical theorem, not arithmetic.

"""

import numpy as np
import itertools
from functools import reduce
from math import gcd
import sympy as sp

TOL = 1e-10

# =============================================================================
# A. REBUILD THE SU(3) FOLD SPECTRUM
# =============================================================================

def gell_mann():
    s3 = np.sqrt(3.0)
    i = 1j
    return [
        np.array([[0,1,0],[1,0,0],[0,0,0]],complex),
        np.array([[0,-i,0],[i,0,0],[0,0,0]],complex),
        np.array([[1,0,0],[0,-1,0],[0,0,0]],complex),
        np.array([[0,0,1],[0,0,0],[1,0,0]],complex),
        np.array([[0,0,-i],[0,0,0],[i,0,0]],complex),
        np.array([[0,0,0],[0,0,1],[0,1,0]],complex),
        np.array([[0,0,0],[0,0,-i],[0,i,0]],complex),
        np.array([[1,0,0],[0,1,0],[0,0,-2]],complex)/s3,
    ]

lam = gell_mann()

def comm_stress(A,B):
    C = A@B-B@A
    return float(np.trace(C.conj().T@C).real)

def stress_sum(indices):
    return sum(
        comm_stress(lam[a],lam[b])
        for ii,a in enumerate(indices)
        for b in indices[ii+1:]
    )

# Fold 1
G1 = stress_sum([0,1,2])

# Fold 2
G2_direct = stress_sum([0,1,2,5,6,7])
G2_bridge = comm_stress(lam[3],lam[4])
G2 = G2_direct + G2_bridge

# Fold 3
G3_raw = stress_sum(list(range(8)))
closure_terms = [
    comm_stress(lam[cg],lam[eg])
    for cg in (3,4)
    for eg in (0,1,5,6)
]
closure = sum(closure_terms)
G3 = G3_raw - closure

assert abs(G1-24)<TOL
assert abs(G2_direct-56)<TOL
assert abs(G2_bridge-8)<TOL
assert abs(G2-64)<TOL
assert abs(G3_raw-96)<TOL
assert len(closure_terms)==8
assert all(abs(x-2)<TOL for x in closure_terms)
assert abs(closure-16)<TOL
assert abs(G3-80)<TOL

GAMMAS = (int(round(G1)),int(round(G2)),int(round(G3)))
assert GAMMAS == (24,64,80)

# =============================================================================
# B. PRIMITIVE DECOMPOSITION
# =============================================================================

s = reduce(gcd,GAMMAS)
a,b,c = tuple(x//s for x in GAMMAS)
assert s == 8
assert (a,b,c) == (3,8,10)

# Crucial internal identity
assert s == b

# Therefore the raw Gamma values are:
assert GAMMAS[0] == s*a == b*a
assert GAMMAS[1] == s*b == b*b
assert GAMMAS[2] == s*c == b*c

# Hence:
internal_5120 = GAMMAS[1]*GAMMAS[2]
primitive_5120 = b**3*c

assert internal_5120 == 5120
assert primitive_5120 == 5120
assert internal_5120 == primitive_5120

# Related exact gaps
assert c-b == 2
assert b-a == 5
assert c-a == 7

# =============================================================================
# C. INDEPENDENT IDEAL HAWKING DERIVATION
# =============================================================================

hbar, clight, kB, R, G, M = sp.symbols("hbar c k_B R G M", positive=True)
pi = sp.pi

Rs = 2*G*M/clight**2
A = 4*pi*R**2
TH = hbar*clight/(4*pi*kB*R)
sigma = pi**2*kB**4/(60*hbar**3*clight**2)

P_R = sp.simplify(A*sigma*TH**4)
assert sp.simplify(P_R-hbar*clight**2/(3840*pi*R**2)) == 0

P_M = sp.simplify(P_R.subs(R,Rs))
assert sp.simplify(P_M-hbar*clight**6/(15360*pi*G**2*M**2)) == 0

Kloss = hbar*clight**4/(15360*pi*G**2)
tH = sp.simplify(M**3/(3*Kloss))
assert sp.simplify(tH-5120*pi*G**2*M**3/(hbar*clight**4)) == 0

# =============================================================================
# D. EXACT INTERNAL / HAWKING COEFFICIENT MATCH
# =============================================================================

HAWKING_LIFETIME_COEFF = 5120

assert internal_5120 == HAWKING_LIFETIME_COEFF

# This is stronger than the primitive-ratio reconstruction because the raw
# Fold-2 and Fold-3 invariants themselves multiply directly:
#
#     Gamma2^2 * Gamma3^2 = 64*80 = 5120.
#
# No reduction to 3:8:10 is required to state this identity.
#
# The primitive reduction explains WHY this product has the compact form:
#
#     Gamma2^2 = b^2
#     Gamma3^2 = b*c
#     product  = b^3*c.

# =============================================================================
# E. WHAT IS ACTUALLY OPEN?
# =============================================================================

# The following are arithmetic/structural facts:
#
# F1. Fold 2 is the first two-seam/composite stage and has Gamma2^2=64.
# F2. Fold 3 is the fully closed SU(3) stage and has Gamma3^2=80.
# F3. Gamma2^2*Gamma3^2 = 5120 exactly.
# F4. Standard ideal Hawking lifetime coefficient is 5120 exactly.
#
# The remaining PHYSICAL claim is:
#
# B3. The physical lifetime functional for evaporation is proportional to
#     (closure stress budget) * (inverse leakage rate/time),
#     with Fold 3 supplying the former and Fold 2 supplying the latter.
#
# Older Ford texts state:
#     Gamma3^2 = stress budget
#     Gamma2^2 = inverse leakage rate
# and motivate multiplication dimensionally.
#
# But unless an explicit dynamical operator / first-passage / decay equation
# derives that assignment, B3 remains a physical interpretation, not a theorem.

# =============================================================================
# F. MINIMAL DYNAMICAL BRIDGE TARGET
# =============================================================================

# A proper bridge theorem could have one of the following forms:
#
# ROUTE 1 — DECAY / FIRST-PASSAGE:
#   derive a Fold-state survival variable X(t) satisfying
#
#       dX/dt = - X / tau_2
#
#   where tau_2 is derived from the Fold-2 response and
#
#       X(0) = Gamma3^2
#
#   then show the integrated lifetime coefficient is Gamma3^2*Gamma2^2.
#
# ROUTE 2 — FLUX BALANCE:
#   derive
#
#       lifetime = stored_closure_budget / leakage_flux
#
#   with
#
#       stored_closure_budget ~ Gamma3^2
#       1/leakage_flux        ~ Gamma2^2
#
#   from the microscopic current operator.
#
# ROUTE 3 — ACTION / HAZARD:
#   derive a hazard rate lambda_2 ~ 1/Gamma2^2 and a total available Fold-3
#   action/budget Gamma3^2, giving total survival time ~ Gamma3^2/lambda_unit.
#
# Any route must derive the role of Gamma2^2 as an inverse rate/time, not assume it.

# =============================================================================
# G. REPORT
# =============================================================================

print("="*126)
print("FORD SU(3) -> HAWKING BRIDGE AUDIT v9")
print("="*126)
print()

print("1. SU(3) FOLD ALGEBRA")
print(f"   Gamma1^2 = {GAMMAS[0]}")
print(f"   Gamma2^2 = {G2_direct:.0f}+{G2_bridge:.0f} = {GAMMAS[1]}")
print(f"   Gamma3^2 = {G3_raw:.0f}-{closure:.0f} = {GAMMAS[2]}")
print()

print("2. PRIMITIVE DECOMPOSITION")
print(f"   gcd s = {s}")
print(f"   primitive triple (a,b,c) = {(a,b,c)}")
print(f"   crucial identity: s=b={b}")
print()
print(f"   Gamma1^2 = s*a = b*a = {b}*{a} = {GAMMAS[0]}")
print(f"   Gamma2^2 = s*b = b^2 = {b}^2 = {GAMMAS[1]}")
print(f"   Gamma3^2 = s*c = b*c = {b}*{c} = {GAMMAS[2]}")
print()

print("3. INTERNAL LIFETIME NUMBER")
print("   Gamma2^2 * Gamma3^2")
print(f"     = {GAMMAS[1]} * {GAMMAS[2]}")
print(f"     = {internal_5120}")
print()
print("   equivalently from primitive structure:")
print("     b^3*c")
print(f"     = {b}^3*{c}")
print(f"     = {primitive_5120}")
print()

print("4. INDEPENDENT IDEAL HAWKING RESULT")
print("   P_H(R) denominator = 3840*pi")
print("   P_H(M) denominator = 15360*pi")
print("   lifetime coefficient = 5120*pi")
print(f"   integer lifetime coefficient = {HAWKING_LIFETIME_COEFF}")
print()

print("5. EXACT MATCH")
print(f"   Gamma2^2 * Gamma3^2 = {internal_5120}")
print(f"   Hawking lifetime integer = {HAWKING_LIFETIME_COEFF}")
print("   residual = 0")
print()

print("6. WHAT HAS BEEN UPGRADED")
print("   Previous status:")
print("     b^2=64 and b^3*c=5120 were treated as declared comparison rules.")
print("   New status:")
print("     both follow internally because s=gcd(24,64,80)=8 and s=b.")
print("     Therefore Gamma2^2=b^2 and Gamma3^2=b*c automatically.")
print("     Their product is forced algebraically to b^3*c=5120.")
print()

print("7. SINGLE REMAINING PHYSICAL BRIDGE")
print("   OPEN B3:")
print("     derive from dynamics that physical black-hole lifetime is")
print("       closure budget x inverse leakage rate/time,")
print("     with")
print("       Fold 3 -> closure budget Gamma3^2")
print("       Fold 2 -> inverse leakage rate/time Gamma2^2.")
print()
print("   The old papers state this interpretation and give dimensional motivation,")
print("   but an explicit microscopic decay/current/first-passage derivation is still needed.")
print()

print("8. STRONGEST CURRENT STATEMENT")
print("   The SU(3) fold algebra independently generates Gamma2^2=64 and")
print("   Gamma3^2=80, whose product is exactly 5120. Standard ideal Hawking")
print("   theory independently gives lifetime coefficient 5120. The equality is")
print("   exact and internally forced arithmetically. The remaining task is to")
print("   derive why Fold-3 closure budget multiplied by the Fold-2 inverse leakage")
print("   timescale is the physical evaporation lifetime.")
print()

print("="*126)
print("ALL ASSERTIONS PASSED")
print("="*126)
