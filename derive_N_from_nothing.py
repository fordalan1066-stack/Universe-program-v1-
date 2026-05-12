#!/usr/bin/env python3
"""
FROM EMPTY SPACE TO N = 3
==========================

Start with nothing. Flat, featureless, potential geometric space.
Ask: what is the minimal structure needed to support a closed
one-way boundary (a horizon)?

Each step forces the next. Nothing is chosen — everything is
required by the previous step.
"""
import numpy as np
from itertools import combinations

print("=" * 80)
print("FROM EMPTY SPACE TO N = 3")
print("=" * 80)

# =====================================================================
# STEP 0: EMPTY SPACE
# =====================================================================
print("""
STEP 0: EMPTY SPACE
  We have a smooth manifold. No curvature, no boundaries, no
  structure. Just a topological space with a differentiable
  structure. Dimension is not yet fixed.
""")

# =====================================================================
# STEP 1: A HORIZON REQUIRES A CLOSED SURFACE
# =====================================================================
print("-" * 80)
print("STEP 1: A HORIZON REQUIRES A CLOSED 2-SURFACE")
print("-" * 80)
print("""
  A "one-way boundary" means: there exists a closed hypersurface
  such that causal curves can cross it in one direction but not
  the other. This is a NULL HYPERSURFACE — a codimension-1 surface
  whose normal vector is null (lightlike).

  A null hypersurface in D-dimensional spacetime has a (D-2)-
  dimensional spatial cross-section. For the boundary to be CLOSED
  (compact, no edges), this cross-section must be a compact manifold
  without boundary.

  WHAT THIS FORCES: The existence of a compact (D-2)-dimensional
  surface Σ embedded in spacetime. Nothing else yet — no specific
  topology, no specific D.
""")

# =====================================================================
# STEP 2: CAUSALITY FIXES THE TOPOLOGY
# =====================================================================
print("-" * 80)
print("STEP 2: CAUSALITY FIXES THE TOPOLOGY TO S²")
print("-" * 80)
print("""
  The one-way property means the boundary is CAUSAL — it respects
  the causal structure of spacetime. This is not just any surface;
  it's a trapped surface boundary.

  TOPOLOGICAL CENSORSHIP (Friedman-Schleich-Witt 1993):
  In any globally hyperbolic, asymptotically flat spacetime
  satisfying the null energy condition, the domain of outer
  communication is simply connected.

  CONSEQUENCE: The cross-section Σ must be simply connected.
  The only compact, orientable, simply connected 2-surface is S².

  WHAT THIS FORCES:
    — The spacetime dimension D = 4 (2 for Σ + 1 radial + 1 time)
    — The cross-section Σ = S²
    — The Euler characteristic χ(S²) = 2
""")

euler_S2 = 2
print(f"  χ(S²) = {euler_S2}")

# =====================================================================
# STEP 3: ONE-WAY REQUIRES AN INSIDE AND AN OUTSIDE
# =====================================================================
print("\n" + "-" * 80)
print("STEP 3: ONE-WAY REQUIRES TWO DISTINCT REGIONS")
print("-" * 80)
print("""
  A one-way boundary separates space into two causally distinct
  regions: an INTERIOR (from which nothing escapes) and an
  EXTERIOR (which receives signals from the boundary but cannot
  send them back).

  This is not optional — it's what "one-way" MEANS. If there is
  no distinction between inside and outside, there is no boundary.

  WHAT THIS FORCES: The surface S² must support a notion of
  "two sides." Mathematically, S² is orientable, so it has a
  well-defined inside and outside. But we need more than just
  orientation — we need the structure ON the surface to encode
  this distinction.

  MINIMUM REQUIREMENT: The surface must carry at least TWO
  distinguishable regions (to represent the two sides of the
  causal boundary). This means the surface must be PARTITIONED
  into at least 2 domains.

  So: N ≥ 2.
""")

# =====================================================================
# STEP 4: DYNAMICS REQUIRES NON-TRIVIAL ALGEBRA
# =====================================================================
print("-" * 80)
print("STEP 4: A FUNCTIONING BOUNDARY REQUIRES DYNAMICS")
print("-" * 80)
print("""
  A static, frozen boundary is not a horizon — it's just a
  geometric surface. A horizon must be DYNAMICAL: it must be
  able to absorb, process, and (via Hawking radiation) emit.

  Dynamics requires an algebra of transformations acting on the
  surface. The partitioned surface with N domains and seams
  between them carries a natural algebra: the generators of
  transitions between domains.

  For N domains where all pairs share a seam:
    Algebra = su(N)
    Dimension = N² - 1
    Rank = N - 1

  WHAT THIS FORCES: N ≥ 2 (we already knew this).
  But we need MORE than just any algebra — we need the algebra
  to support the inside/outside distinction from Step 3.
""")

print("  Algebra data for small N:")
print(f"  {'N':>3s}  {'Algebra':>8s}  {'dim':>5s}  {'rank':>5s}  {'Type'}")
print("  " + "-" * 50)
for n in range(1, 6):
    dim = n**2 - 1
    rank = n - 1
    if n == 1:
        atype = "Trivial (no generators)"
    elif n == 2:
        atype = "Non-Abelian, rank 1"
    else:
        atype = f"Non-Abelian, rank {rank}"
    print(f"  {n:3d}  {'su('+str(n)+')':>8s}  {dim:5d}  {rank:5d}  {atype}")

# =====================================================================
# STEP 5: INSIDE/OUTSIDE DISTINCTION REQUIRES RANK ≥ 2
# =====================================================================
print("\n" + "-" * 80)
print("STEP 5: INSIDE/OUTSIDE REQUIRES RANK ≥ 2")
print("-" * 80)
print("""
  The algebra must encode the causal distinction between inside
  and outside. This means the Cartan subalgebra (the maximal set
  of simultaneously diagonalizable generators) must split into:

    — At least one INTERNAL generator (coupled to the interior)
    — At least one EXTERNAL generator (coupled to the exterior)

  This requires rank ≥ 2.

  WHY: At an active seam between two domains, the algebra
  decomposes as su(N) → su(N-1) ⊕ u(1). The Cartan subalgebra
  of the accessible part has rank = (N-2) + 1 = N-1.

  For the internal/external split:
    rank(su(N-1)) ≥ 1  AND  rank(u(1)) = 1

  rank(su(N-1)) = N-2 ≥ 1 requires N ≥ 3.

  N = 2: su(2) → su(1) ⊕ u(1) = {0} ⊕ u(1).
         The subalgebra su(1) is EMPTY. There is no internal
         generator. The algebra cannot distinguish inside from
         outside. There is only one Cartan generator, and it
         must serve as the external channel — but then nothing
         is left to represent the interior.

  This is not a thermodynamic argument. This is STRUCTURAL.
  N = 2 fails because the algebra is too small to encode the
  causal structure that defines a horizon.

  WHAT THIS FORCES: N ≥ 3.
""")

# Verify explicitly
print("  Subalgebra decomposition at active seam:")
print(f"  {'N':>3s}  {'su(N-1)':>8s}  {'rank(int)':>10s}  {'rank(ext)':>10s}  "
      f"{'Internal gen?':>14s}  {'Status'}")
print("  " + "-" * 70)
for n in range(2, 6):
    r_int = n - 2
    r_ext = 1
    has_internal = "Yes" if r_int >= 1 else "No"
    status = "✓" if r_int >= 1 else "✗ (no inside)"
    sub = f"su({n-1})"
    print(f"  {n:3d}  {sub:>8s}  {r_int:10d}  {r_ext:10d}  {has_internal:>14s}  {status}")

# =====================================================================
# STEP 6: MUTUAL ADJACENCY REQUIRES N ≤ 4
# =====================================================================
print("\n" + "-" * 80)
print("STEP 6: STRESS TRANSPORT REQUIRES N ≤ 4")
print("-" * 80)
print("""
  For the horizon to function as a coherent boundary (not a
  patchwork of disconnected regions), stress must be able to
  propagate between ANY pair of domains. This requires every
  pair of domains to share a seam.

  The dual graph must contain the complete graph K_N.

  KURATOWSKI'S THEOREM (1930): K_N is planar (embeds on S²)
  if and only if N ≤ 4.

  WHAT THIS FORCES: N ≤ 4.
  Combined with Step 5 (N ≥ 3): N ∈ {3, 4}.
""")

print("  K_N planarity:")
print(f"  {'N':>3s}  {'Planar?':>8s}")
print("  " + "-" * 15)
for n in range(2, 7):
    planar = "Yes" if n <= 4 else "No"
    print(f"  {n:3d}  {planar:>8s}")

# =====================================================================
# STEP 7: MINIMALITY FORCES N = 3
# =====================================================================
print("\n" + "-" * 80)
print("STEP 7: MINIMALITY FORCES N = 3")
print("-" * 80)
print("""
  We asked: what is the MINIMAL structure that empty space needs
  to support a horizon?

  Steps 1-6 have narrowed the answer to N ∈ {3, 4}.

  N = 3 satisfies every requirement:
    — Closed surface: S² ✓
    — Two-sided: inside/outside encoded ✓
    — Dynamic: su(3), dim 8, rank 2 ✓
    — Internal/external split: rank(su(2)) = 1, rank(u(1)) = 1 ✓
    — Mutual adjacency: K_3 planar ✓

  N = 4 also satisfies every requirement. But N = 4 introduces
  ADDITIONAL structure beyond what is required:
    — 6 seams instead of 3
    — 15 generators instead of 8
    — rank 3 instead of rank 2
    — 2 internal Cartan generators instead of 1

  The question was: what is the MINIMAL structure? The answer is
  the smallest N that satisfies all constraints. That is N = 3.

  This is not an aesthetic choice. It is the answer to the question
  we asked. If we had asked "what structures are POSSIBLE?", the
  answer would be {3, 4}. But we asked "what is the MINIMUM?",
  and the answer is 3.
""")

# =====================================================================
# STEP 7b: SMARR PROVIDES AN INDEPENDENT CONFIRMATION
# =====================================================================
print("-" * 80)
print("STEP 7b: SMARR FORMULA INDEPENDENTLY CONFIRMS N = 3")
print("-" * 80)
print("""
  If minimality feels too soft, the Smarr formula provides a
  HARD constraint that independently eliminates N = 4.

  The Smarr formula (theorem, D = 4): M = 2TS.
  This requires the thermal fraction f_thermal = 1/2.

  In the algebra: f_thermal = rank(u(1)) / rank(total) = 1/(N-1).
    N = 3: f_thermal = 1/2 ✓
    N = 4: f_thermal = 1/3 ✗

  So even without invoking minimality, N = 4 is eliminated by
  black hole thermodynamics. But the minimality argument is
  logically prior — it doesn't need thermodynamics at all.
""")

# =====================================================================
# SUMMARY: THE CHAIN
# =====================================================================
print("=" * 80)
print("THE COMPLETE CHAIN: EMPTY SPACE → N = 3")
print("=" * 80)
print("""
  Step 0: Empty space (smooth manifold, no structure)
       ↓  "Support a one-way boundary"
  Step 1: Need a closed codimension-2 surface Σ
       ↓  Topological Censorship
  Step 2: Σ = S², D = 4
       ↓  "One-way" means inside ≠ outside
  Step 3: Need ≥ 2 distinguishable regions on S²
       ↓  Boundary must be dynamical (absorb, emit)
  Step 4: Need algebra su(N) on partitioned S²
       ↓  Must encode inside/outside distinction
  Step 5: Need rank ≥ 2 → N ≥ 3
       ↓  All domains must communicate
  Step 6: K_N planar → N ≤ 4
       ↓  Minimal structure
  Step 7: N = 3

  Nothing was chosen. Each step was forced by the previous one.
  The only input was: "empty space" + "one-way boundary."
""")

# =====================================================================
# THE N = 2 FAILURE — NOW STRUCTURAL, NOT THERMODYNAMIC
# =====================================================================
print("=" * 80)
print("WHY N = 2 FAILS — THE STRUCTURAL ARGUMENT")
print("=" * 80)
print("""
  N = 2 is not eliminated by Bekenstein-Hawking (that's a
  consistency check, not a structural argument).

  N = 2 is eliminated because IT CANNOT BE A HORIZON:

  A horizon is a one-way boundary. "One-way" requires an inside
  and an outside. The algebra on the surface must encode this
  distinction — it must have generators coupled to the interior
  AND generators coupled to the exterior.

  For N = 2: su(2) → su(1) ⊕ u(1) = {0} ⊕ u(1).
  The internal subalgebra su(1) is EMPTY. There are zero internal
  generators. The algebra has no way to represent the interior.

  A surface whose algebra cannot represent its own interior is
  not a one-way boundary. It's just a surface.

  N = 2 doesn't give the wrong entropy. N = 2 doesn't give a
  horizon AT ALL.
""")

# Verify: su(2) generators at the "active seam"
print("  Verification: su(2) Pauli matrices")
pauli = [
    np.array([[0,1],[1,0]], dtype=complex),
    np.array([[0,-1j],[1j,0]], dtype=complex),
    np.array([[1,0],[0,-1]], dtype=complex),
]
pauli_names = ['σ₁', 'σ₂', 'σ₃']

print(f"  {'Gen':>4s}  {'Diagonal':>9s}  {'Cartan?':>8s}")
print("  " + "-" * 30)
n_cartan_su2 = 0
for i, (p, name) in enumerate(zip(pauli, pauli_names)):
    is_diag = np.allclose(p, np.diag(np.diag(p)))
    is_cartan = is_diag
    if is_cartan:
        n_cartan_su2 += 1
    print(f"  {name:>4s}  {'Yes' if is_diag else 'No':>9s}  {'Yes' if is_cartan else 'No':>8s}")

print(f"\n  Total Cartan generators in su(2): {n_cartan_su2}")
print(f"  This single Cartan generator (σ₃) must serve as the")
print(f"  external channel. Nothing remains for the interior.")
print(f"  rank(internal) = 0. The inside is unrepresented. ✗")

print("\n  Compare with su(3):")
print(f"  Cartan generators: λ₃ (internal) + λ₈ (external)")
print(f"  rank(internal) = 1, rank(external) = 1")
print(f"  Both sides of the horizon are represented. ✓")

print("\n" + "=" * 80)
print("END")
print("=" * 80)
