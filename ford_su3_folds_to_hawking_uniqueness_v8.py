#!/usr/bin/env python3
"""
FORD SU(3) FOLDS -> HAWKING RATIO / UNIQUENESS AUDIT
=====================================================
Purpose
-------
Rebuild the Ford fold-stress numbers 24, 64, 80 directly from the standard
Gell-Mann matrices; freeze that result; independently derive the ideal
Schwarzschild Hawking coefficients; and only then compare the two sides.

Status discipline
-----------------
EXACT ALGEBRA:
    direct matrix / symbolic identities.

MODEL PRESCRIPTION:
    which SU(3) generator subsets correspond to Fold 1, Fold 2, Fold 3, and
    the closure-redundancy subtraction. The matrix consequences of that
    prescription are exact, but the physical interpretation of folds as
    successive 3D-axis/access stages is additional model structure.

EXACT CORRESPONDENCE:
    numerical/relational equality between independently computed sides.

CONDITIONAL PHYSICAL EQUIVALENCE:
    requires a principled map showing why the corresponding factors represent
    the same physical operation, not merely the same integer.

The Hawking comparison is to the ideal Schwarzschild blackbody baseline.
Greybody/species corrections are a separate problem.
"""

import itertools
from functools import reduce
from math import gcd
import numpy as np
import sympy as sp

TOL = 1e-10

# ============================================================================
# A. STANDARD SU(3) ALGEBRA
# ============================================================================

def gell_mann_matrices():
    """Standard Gell-Mann matrices with Tr(lambda_a lambda_b)=2 delta_ab."""
    z = 0.0
    i = 1j
    s3 = np.sqrt(3.0)
    return [
        np.array([[0,1,0],[1,0,0],[0,0,0]], dtype=complex),                 # λ1
        np.array([[0,-i,0],[i,0,0],[0,0,0]], dtype=complex),                # λ2
        np.array([[1,0,0],[0,-1,0],[0,0,0]], dtype=complex),                # λ3
        np.array([[0,0,1],[0,0,0],[1,0,0]], dtype=complex),                 # λ4
        np.array([[0,0,-i],[0,0,0],[i,0,0]], dtype=complex),                # λ5
        np.array([[0,0,0],[0,0,1],[0,1,0]], dtype=complex),                 # λ6
        np.array([[0,0,0],[0,0,-i],[0,i,0]], dtype=complex),                # λ7
        np.array([[1,0,0],[0,1,0],[0,0,-2]], dtype=complex)/s3,             # λ8
    ]

lam = gell_mann_matrices()

# Verify normalization.
for a in range(8):
    for b in range(8):
        got = np.trace(lam[a] @ lam[b])
        expected = 2.0 if a == b else 0.0
        assert abs(got - expected) < TOL

def commutator(A, B):
    return A @ B - B @ A

def pair_stress(A, B):
    C = commutator(A, B)
    return float(np.real(np.trace(C.conj().T @ C)))

def stress_invariant(indices):
    """Gamma^2 = sum_{a<b} Tr([lambda_a,lambda_b]^dagger [...])."""
    total = 0.0
    contributions = []
    for p, q in itertools.combinations(indices, 2):
        w = pair_stress(lam[p], lam[q])
        total += w
        contributions.append((p+1, q+1, w))
    return total, contributions

# ============================================================================
# B. MODEL FOLD PRESCRIPTION -> 24, 64, 80
# ============================================================================

# Fold 1:
# first elementary seam 1<->2, using its SU(2) pipe subalgebra λ1,λ2,λ3.
fold1_indices = [0,1,2]
G1, fold1_pairs = stress_invariant(fold1_indices)
assert abs(G1 - 24.0) < TOL

# Fold 2:
# two elementary seams active. Direct set λ1,λ2,λ3,λ6,λ7,λ8 gives 56.
# Closure of the two elementary seams generates the composite 1<->3 seam;
# the composite self-interaction [λ4,λ5] contributes 8.
fold2_direct_indices = [0,1,2,5,6,7]
G2_direct, fold2_pairs = stress_invariant(fold2_direct_indices)
composite_self = pair_stress(lam[3], lam[4])
G2 = G2_direct + composite_self
assert abs(G2_direct - 56.0) < TOL
assert abs(composite_self - 8.0) < TOL
assert abs(G2 - 64.0) < TOL

# Fold 3:
# all three seams/full SU(3) accessible. Raw all-pair stress is 96.
# Model closure prescription removes the eight redundant composite-vs-elementary
# pipe pairs: (λ4,λ5) x (λ1,λ2,λ6,λ7). Each contributes 2 -> total 16.
G3_raw, fold3_pairs = stress_invariant(list(range(8)))
composite_indices = [3,4]
elementary_pipe_indices = [0,1,5,6]
closure_terms = []
closure_correction = 0.0
for cg in composite_indices:
    for eg in elementary_pipe_indices:
        w = pair_stress(lam[cg], lam[eg])
        closure_terms.append((cg+1, eg+1, w))
        closure_correction += w

G3 = G3_raw - closure_correction
assert abs(G3_raw - 96.0) < TOL
assert len(closure_terms) == 8
assert all(abs(w-2.0) < TOL for _,_,w in closure_terms)
assert abs(closure_correction - 16.0) < TOL
assert abs(G3 - 80.0) < TOL

FORD_RAW = tuple(int(round(x)) for x in (G1,G2,G3))
assert FORD_RAW == (24,64,80)

common = reduce(gcd, FORD_RAW)
FORD_PRIMITIVE = tuple(x//common for x in FORD_RAW)
assert common == 8
assert FORD_PRIMITIVE == (3,8,10)

a,b,c = FORD_PRIMITIVE
d = c-b
assert d == 2

# Freeze Ford result before Hawking side.
FORD_FREEZE = {
    "raw_stiffness": FORD_RAW,
    "gcd": common,
    "primitive_ratio": FORD_PRIMITIVE,
    "adjacent_upper_gap": d,
}

# ============================================================================
# C. INDEPENDENT IDEAL HAWKING DERIVATION
# ============================================================================

hbar, clight, kB, R, G, M = sp.symbols(
    "hbar c k_B R G M", positive=True
)
pi = sp.pi

R_s = 2*G*M/clight**2
A = 4*pi*R**2
T_R = hbar*clight/(4*pi*kB*R)
sigma = pi**2*kB**4/(60*hbar**3*clight**2)

P_R = sp.simplify(A*sigma*T_R**4)
P_R_expected = hbar*clight**2/(3840*pi*R**2)
assert sp.simplify(P_R-P_R_expected) == 0

P_M = sp.simplify(P_R.subs(R,R_s))
P_M_expected = hbar*clight**6/(15360*pi*G**2*M**2)
assert sp.simplify(P_M-P_M_expected) == 0

# c^2 dM/dt = -P_M, so lifetime:
loss_coeff = hbar*clight**4/(15360*pi*G**2)
lifetime = sp.simplify(M**3/(3*loss_coeff))
lifetime_expected = 5120*pi*G**2*M**3/(hbar*clight**4)
assert sp.simplify(lifetime-lifetime_expected) == 0

H_RADIUS = 3840
H_MASS = 15360
H_LIFE = 5120
H_SB = 60
H_TEMP_M = 8
H_SCHW = 2
H_INTEGRAL = 3

assert H_RADIUS == 64*60
assert H_MASS == H_RADIUS*4
assert H_LIFE == H_MASS//3

# ============================================================================
# D. EXACT FORD-RATIO -> HAWKING RECONSTRUCTION
# ============================================================================

assert b**2 == 64
assert a*c*d == 60
assert a*b**2*c*d == H_RADIUS
assert a*b**3*c == H_MASS
assert b**3*c == H_LIFE

# Hawking transformation chain expressed in primitive Ford variables:
assert d**2 == 4
assert H_RADIUS * d**2 == H_MASS
assert H_MASS // a == H_LIFE

# ============================================================================
# E. REVERSE HAWKING -> 3:8:10
# ============================================================================

# Using independently meaningful ideal-Hawking integers:
#   64 = residual area/T^4 block
#   5120 = lifetime coefficient
#   60 = Stefan-Boltzmann denominator
#
# Under the declared mapping rules:
#   b^2 = 64
#   b^3 c = 5120
#   a c (c-b) = 60
#
# positivity makes the solution analytic and unique.

b_rev = int(sp.sqrt(64))
assert b_rev > 0 and b_rev**2 == 64

c_rev = H_LIFE // (b_rev**3)
assert b_rev**3 * c_rev == H_LIFE

d_rev = c_rev - b_rev
assert d_rev > 0

a_rev = H_SB // (c_rev*d_rev)
assert a_rev*c_rev*d_rev == H_SB

HAWKING_PRIMITIVE = (a_rev,b_rev,c_rev)
assert HAWKING_PRIMITIVE == (3,8,10)
assert HAWKING_PRIMITIVE == FORD_PRIMITIVE

# Cross-check with direct familiar Hawking integers:
assert a_rev == H_INTEGRAL
assert b_rev == H_TEMP_M
assert d_rev == H_SCHW
assert c_rev == H_TEMP_M + H_SCHW
assert c_rev == H_SB//(H_INTEGRAL*H_SCHW)

# ============================================================================
# F. ANALYTIC UNIQUENESS THEOREM WITHIN DECLARED MAPPING RULES
# ============================================================================

# Let a,b,c be positive reals/integers with c>b and require:
#   b^2 = 64
#   b^3 c = 5120
#   a c(c-b) = 60
#
# Positive b is forced to 8.
# Then c is forced to 10.
# Then a is forced to 3.
# There is no search cutoff.

b_sym, c_sym, a_sym = sp.symbols("b c a", positive=True)
b_forced = sp.sqrt(64)
c_forced = sp.Rational(5120,1)/(b_forced**3)
a_forced = sp.Rational(60,1)/(c_forced*(c_forced-b_forced))
assert sp.simplify(b_forced-8) == 0
assert sp.simplify(c_forced-10) == 0
assert sp.simplify(a_forced-3) == 0

# ============================================================================
# G. ADVERSARIAL CHECK: ARE THE MAPPING RULES THEMSELVES FORCED?
# ============================================================================

# This script deliberately does NOT claim they are.
# The uniqueness theorem says:
#     IF the physically justified comparison rules are
#        b^2=64, b^3 c=5120, a c(c-b)=60,
#     THEN 3:8:10 is uniquely forced.
#
# The remaining physics theorem must justify those rule choices by role
# independently of the numerical success.

# ============================================================================
# H. REPORT
# ============================================================================

def show_pairs(title, pairs):
    print(title)
    for p,q,w in pairs:
        if abs(w) > TOL:
            print(f"    (lambda_{p}, lambda_{q}) -> {w:g}")

print("="*124)
print("FORD SU(3) FOLDS -> HAWKING RATIO / UNIQUENESS AUDIT")
print("="*124)
print()

print("A. SU(3) FOLD DERIVATION")
print("  Fold 1:")
show_pairs("    nonzero pair stresses:", fold1_pairs)
print(f"    Gamma_1^2 = {G1:.0f}")
print()
print("  Fold 2:")
print(f"    direct six-generator stress = {G2_direct:.0f}")
print(f"    composite [lambda_4,lambda_5] self-stress = {composite_self:.0f}")
print(f"    Gamma_2^2 = {G2_direct:.0f}+{composite_self:.0f} = {G2:.0f}")
print()
print("  Fold 3:")
print(f"    raw full-SU(3) all-pair stress = {G3_raw:.0f}")
print(f"    redundant closure pairs = {len(closure_terms)}")
print(f"    each redundant pair stress = 2")
print(f"    closure correction = {closure_correction:.0f}")
print(f"    Gamma_3^2 = {G3_raw:.0f}-{closure_correction:.0f} = {G3:.0f}")
print()
print(f"  FROZEN Ford spectrum = {FORD_RAW}")
print(f"  gcd = {common}")
print(f"  primitive ratio = {FORD_PRIMITIVE[0]}:{FORD_PRIMITIVE[1]}:{FORD_PRIMITIVE[2]}")
print(f"  upper adjacent gap c-b = {d}")
print()

print("B. INDEPENDENT IDEAL HAWKING DERIVATION")
print("  A = 4*pi*R^2")
print("  T_H(R) = hbar*c/(4*pi*k_B*R)")
print("  sigma_SB = pi^2*k_B^4/(60*hbar^3*c^2)")
print("  P_H(R) = hbar*c^2/(3840*pi*R^2)")
print("  R_s = 2GM/c^2")
print("  P_H(M) = hbar*c^6/(15360*pi*G^2*M^2)")
print("  lifetime = 5120*pi*G^2*M^3/(hbar*c^4)")
print()

print("C. EXACT RATIO LINK")
print("  Let (a,b,c) = (3,8,10), d=c-b=2")
print("  b^2 = 8^2 = 64")
print("  a*c*d = 3*10*2 = 60")
print("  radius denominator:")
print("    a*b^2*c*d = 3*8^2*10*2 = 3840")
print("  mass denominator:")
print("    a*b^3*c = 3*8^3*10 = 15360")
print("  lifetime coefficient:")
print("    b^3*c = 8^3*10 = 5120")
print("  Hawking transformation chain:")
print("    3840 --x(c-b)^2=x4--> 15360 --/a=/3--> 5120")
print()

print("D. REVERSE HAWKING CLOSURE")
print("  b^2=64 -> positive b=8")
print("  b^3*c=5120 -> c=10")
print("  a*c*(c-b)=60 -> a=3")
print("  therefore Hawking -> unique primitive triple (3,8,10)")
print("  cross-check: c-b=2 equals Schwarzschild-radius integer")
print("  cross-check: a=3 equals lifetime integration integer")
print("  cross-check: b=8 equals mass-form Hawking-temperature integer")
print("  cross-check: 60=3*10*2")
print()

print("E. UNIQUENESS STATUS")
print("  PROVED within declared mapping rules:")
print("    positive solution to")
print("      b^2=64")
print("      b^3*c=5120")
print("      a*c*(c-b)=60")
print("    is uniquely (a,b,c)=(3,8,10).")
print("  No brute-force cutoff is used.")
print()
print("  NOT YET PROVED:")
print("    that these mapping rules are themselves uniquely forced by physics.")
print("    That is now the central bridge theorem.")
print()

print("F. GEOMETRIC/FOLD STATUS")
print("  Model interpretation: three folds are successive access/closure stages")
print("  associated with resolving the three spatial axes of the 3D construction.")
print("  The SU(3) matrix consequences above are exact once that fold prescription")
print("  and the Fold-3 closure redundancy rule are specified.")
print("  A separate derivation should still establish the geometry -> generator-subset")
print("  map rather than assuming it.")
print()

print("G. STRONGEST CAREFUL RESULT")
print("  The model fold prescription generates SU(3) stress spectrum 24:64:80,")
print("  whose primitive ratio is exactly 3:8:10. Independently, the ideal")
print("  Schwarzschild Hawking coefficient chain satisfies a closed set of declared")
print("  factor relations whose unique positive solution is exactly 3:8:10.")
print("  The numerical/relational correspondence is exact. The remaining task is")
print("  to prove the factor-role mapping physically, independently of the match.")
print()
print("="*124)
print("ALL ASSERTIONS PASSED")
print("="*124)
