"""
Ford–String Bridge v8 — repair v7 using the later two-sided relational-transition mechanism.

v7 incorrectly demanded an absolute fixed state L v = v.
Later Ford work uses:
    X = rho * Xhat
    a = d ln rho
so absolute magnitude may evolve while relational structure closes.

Use the completed Ford horizon return
    L = diag(25/18,11/18,11/18,1/6)
on the complete local string (g,B) coefficient block
    v=(m,x,y,b).

Test:
1. Absolute side evolves freely by L; do NOT demand m'=m.
2. Quotient by common magnitude m to relational variables q=(x/m,y/m,b/m).
3. Retain the discarded magnitude change as a = Delta ln m.
4. Ask whether the relational map has a unique attracting closed state and whether
   (q,a) contains the full one-step information needed to reconstruct the next state
   given the current anchor m.
"""
import sympy as sp, json
from pathlib import Path
OUT=Path("/mnt/data")
RESULTS=OUT/"ford_string_bridge_v8_two_sided_closure_results.json"

lc=sp.Rational(25,18)
ls=sp.Rational(11,18)
lo=sp.Rational(1,6)
L=sp.diag(lc,ls,ls,lo)

m,x,y,b=sp.symbols("m x y b", positive=True)
# x,y,b need not physically be positive; symbolic positivity is irrelevant to ratios here.
q1,q2,q3=sp.symbols("q1 q2 q3", real=True)

# Relative return factors.
rs=sp.simplify(ls/lc)
ro=sp.simplify(lo/lc)
assert rs==sp.Rational(11,25)
assert ro==sp.Rational(3,25)
R=sp.diag(rs,rs,ro)

# Unique relational fixed point.
fixed=(R-sp.eye(3)).nullspace()
assert len(fixed)==0  # homogeneous fixed equation has only zero vector

# Common log increment retained by the two-sided representation.
a=sp.log(lc)

# Reconstruction test.
# Current state v = m*(1,q1,q2,q3); after absolute L:
v=sp.Matrix([m,m*q1,m*q2,m*q3])
vp=sp.simplify(L*v)
mp=sp.simplify(sp.exp(a)*m)
qp=sp.simplify(R*sp.Matrix([q1,q2,q3]))
recon=sp.Matrix([mp,mp*qp[0],mp*qp[1],mp*qp[2]])
assert sp.simplify(vp-recon)==sp.zeros(4,1)

# Complete first-cycle quadratic balance inherited from horizon map.
common_raw=lc
relative_raw=2*ls+lo
assert common_raw==relative_raw

result={
 "branch":"Ford–String Bridge v8 — two-sided closure",
 "repair_of_v7":{
   "old_condition":"L v = v on the absolute string modulus state",
   "old_condition_status":"REJECTED as the wrong closure criterion for the later Ford mechanism",
   "later_condition":"absolute magnitude rho may evolve; relational state Xhat closes while a = Delta ln rho retains magnitude change"
 },
 "absolute_side":{
   "return_L":str(L),
   "common_update":"m'=(25/18)m",
   "log_scale_increment":"a=ln(25/18)",
   "absolute_fixed_radius_required":False
 },
 "relational_side":{
   "q_definition":"q=(x/m,y/m,b/m)",
   "return_R":str(R),
   "shape_factor":"11/25",
   "orientation_factor":"3/25",
   "unique_fixed_state":"q*=(0,0,0)",
   "interpretation":"isotropic metric and zero relative B/orientation, with common magnitude not discarded"
 },
 "information_check":{
   "representation":"(m,q) -> (q,a) plus current absolute anchor m",
   "one_step_reconstruction_exact":True,
   "reconstructed_next_state":str(recon),
   "absolute_information_lost_in_one_step":False
 },
 "complete_return":{
   "raw_common_response":str(common_raw),
   "raw_relative_response":str(relative_raw),
   "first_cycle_balance":"EXACT: common = total non-common = 25/18"
 },
 "strict_verdict":{
   "v7_last_modulus_obstruction":"REMOVED as an obstruction to relational closure",
   "relational_modulus_selection":"PASS",
   "absolute_radius_selection":"NOT REQUIRED by this mechanism and NOT produced",
   "what_is_fixed":"the relational vacuum/shape: all three non-common g+B moduli have a unique attracting state",
   "what_evolves":"the common absolute scale, whose change is retained as a logarithmic scale connection rather than treated as an unfixed missing equation",
   "does_this_prove_full_string_vacuum_selection":"NO — it proves closure for this explicit local T2-like g+B modulus block under the Ford return; extension to a full compactification with dilaton, fluxes, complex structure/topology and quantum consistency is a separate test.",
   "key_result":"The apparent final modulus left by v7 arose from imposing absolute fixed-point closure. Under the later Ford two-sided definition, the same complete return closes relationally with no leftover local g+B modulus while preserving the common scale evolution as a."
 }
}
RESULTS.write_text(json.dumps(result,indent=2),encoding="utf-8")
print("="*96)
print("FORD–STRING BRIDGE v8 — TWO-SIDED CLOSURE")
print("="*96)
print("Absolute common update: m' = (25/18)m")
print("Retained log-scale increment: a = ln(25/18)")
print("Relational return:",R)
print("Unique relational fixed state: q=(0,0,0)")
print("One-step reconstruction from relational update + scale increment: PASS")
print("First-cycle common/non-common balance: PASS")
print()
print("STRICT RESULT:")
print("v7's 'last free modulus' is not a failure of relational closure under the later Ford mechanism.")
print("The local g+B relational moduli close; common absolute scale evolves and is retained as d ln rho.")
print("This does not yet establish full string vacuum selection beyond this explicit block.")
