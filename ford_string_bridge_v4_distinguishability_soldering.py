"""
Ford–String Bridge v4
Distinguishability soldering gate for the explicit three-Kähler-modulus no-scale control.

Question
--------
Can the NEW Ford horizon distinguishability law supply the missing relational constraint
to the SAME string Kähler problem, without adding the old Ford Hessian as an external
potential and without fixing the absolute/common string modulus?

String side (unchanged)
-----------------------
K = - sum_i log(T_i + T_i_bar)
real tau_i > 0
log coordinates y_i=ln tau_i
canonical orthogonal coordinates:
  c  = (y1+y2+y3)/sqrt(3)
  s1 = (y1-y2)/sqrt(2)
  s2 = (y1+y2-2y3)/sqrt(6)
G = I/4 and leading no-scale potential is flat in these Kähler directions.

Ford side (already derived)
---------------------------
Actual horizon/tangent completed return has normalized sectors
  common:       1      multiplicity 1
  shape:        11/25  multiplicity 2
  orientation:  3/25  multiplicity 1
and after one cycle
  2*(11/25)+3/25 = 1.

This gate DOES NOT identify the string shapes with all three Ford relative modes.
The string Kähler metric has exactly TWO real shape directions, so only the Ford
two-dimensional horizon shape eigenspace can be canonically dimension-matched.
The Ford orientation mode has no counterpart in this real Kähler slice and is kept separate.

We therefore test two candidate solderings:
 A. honest Kähler-shape soldering: two string shapes <-> two Ford shape modes only.
 B. complete Ford horizon balance: shape + orientation <-> complete non-common sector.

If only B produces the exact 50/50 event, then the new law cannot close the isolated
Kähler slice by itself; the missing orientation/Fields degree must be present in the
complete state. That would directly test the user's claim that the isolated Kähler
calculation was missing parameters from the rest of the model.
"""
import sympy as sp, json, math
from pathlib import Path
OUT=Path("/mnt/data")
RESULTS=OUT/"ford_string_bridge_v4_distinguishability_soldering_results.json"

# ---------- Standard string-side control ----------
t1,t2,t3=sp.symbols("t1 t2 t3", positive=True)
G_tau=sp.diag(*[sp.Rational(1,4)/t**2 for t in (t1,t2,t3)])
Kgrad=sp.Matrix([-sp.Rational(1,2)/t for t in (t1,t2,t3)])
Ginv=sp.diag(*[4*t**2 for t in (t1,t2,t3)])
no_scale=sp.simplify((Kgrad.T*Ginv*Kgrad)[0])
assert no_scale==3

Gy=sp.eye(3)/4
sqrt=sp.sqrt
Q=sp.Matrix([
 [1/sqrt(3),1/sqrt(3),1/sqrt(3)],
 [1/sqrt(2),-1/sqrt(2),0],
 [1/sqrt(6),1/sqrt(6),-2/sqrt(6)]
])
Gq=sp.simplify(Q*Gy*Q.T)
assert Gq==sp.eye(3)/4
H_string=sp.zeros(3)

# ---------- Ford horizon distinguishability ----------
lam_s=sp.Rational(11,25)
lam_o=sp.Rational(3,25)

# A: only the two shape directions available on the real Kähler slice.
R_kahler_shape_1 = 2*lam_s
p_common_kahler = sp.simplify(1/(1+R_kahler_shape_1))
angle_kahler = math.atan(math.sqrt(float(R_kahler_shape_1)))

# B: complete Ford non-common horizon sector.
R_complete_1 = 2*lam_s + lam_o
p_common_complete = sp.simplify(1/(1+R_complete_1))
angle_complete = math.atan(math.sqrt(float(R_complete_1)))
assert R_complete_1==1
assert p_common_complete==sp.Rational(1,2)
assert abs(angle_complete-math.pi/4)<1e-15

# Exact deficit if one incorrectly tries to close with Kähler shape sector alone.
balance_deficit = sp.simplify(1-R_kahler_shape_1)
assert balance_deficit==lam_o  # precisely the omitted orientation sector.

# General n-cycle comparison.
rows=[]
for n in range(0,7):
    Rs=2*float(lam_s**n)
    Ro=float(lam_o**n)
    Rtot=Rs+Ro
    rows.append({
      "n":n,
      "kahler_shape_relative_weight":Rs,
      "omitted_orientation_weight":Ro,
      "complete_relative_weight":Rtot,
      "complete_common_fraction":1/(1+Rtot),
      "complete_distinguishability_angle":math.atan(math.sqrt(Rtot)),
    })

# A local string shape vector can be measured by its string-derived metric:
# ||ds_shape||^2 = (ds1^2+ds2^2)/4.
# Under the Ford horizon shape return, both directions scale by 11/25,
# so the squared string-metric norm scales by (11/25)^2 if interpreted
# as a tangent-vector map. We record compatibility only; this is not a potential.
s1,s2=sp.symbols("s1 s2", real=True)
shape_norm2=(s1**2+s2**2)/4
shape_norm2_after=sp.simplify(((lam_s*s1)**2+(lam_s*s2)**2)/4)
norm_ratio=sp.simplify(shape_norm2_after/shape_norm2)
assert norm_ratio==lam_s**2

result={
 "branch":"Ford–String Bridge v4 — distinguishability soldering",
 "string_side":{
   "no_scale_identity":str(no_scale),
   "metric_common_shape":str(Gq),
   "leading_Kahler_hessian":str(H_string),
   "common_direction":"c=(ln t1+ln t2+ln t3)/sqrt(3)",
   "shape_directions":[
      "s1=ln(t1/t2)/sqrt(2)",
      "s2=ln(t1*t2/t3^2)/sqrt(6)"
   ],
   "absolute_common_modulus":"still unfixed; no new potential inserted"
 },
 "ford_side":{
   "horizon_spectrum":"1 x1, 11/25 x2, 3/25 x1",
   "complete_first_cycle_balance":"2*(11/25)+3/25=1",
   "complete_common_fraction":"1/2",
   "complete_angle":"pi/4"
 },
 "soldering_test":{
   "two_string_shapes_to_two_Ford_shape_modes":"dimensionally canonical local match",
   "shape_only_relative_weight_at_first_cycle":str(R_kahler_shape_1),
   "shape_only_common_fraction":str(p_common_kahler),
   "shape_only_angle_rad":angle_kahler,
   "shape_only_fails_50_50":True,
   "exact_missing_weight":str(balance_deficit),
   "exact_missing_weight_equals_Ford_orientation":"3/25",
   "complete_relative_weight":str(R_complete_1),
   "complete_common_fraction":str(p_common_complete),
   "complete_angle":"pi/4",
   "string_shape_metric_norm_ratio_under_shape_return":str(norm_ratio)
 },
 "cycles":rows,
 "verdict":{
   "isolated_Kahler_distinguishability_closure":"FAIL",
   "complete_state_distinguishability_closure":"STRUCTURAL PASS",
   "key_exact_result":"The isolated two-shape Kähler sector supplies 22/25 of the required first-cycle relative weight. The deficit is exactly 3/25, which is the Ford orientation sector omitted by the isolated Kähler slice.",
   "interpretation":"The exact 50/50 distinction boundary is recovered only when the third, orientation/Fields-type non-common degree is restored. This is direct mathematical support for the diagnosis that the isolated Kähler calculation lacked a parameter carried by the rest of the Ford state.",
   "what_is_not_proved":"We have not yet derived that the Ford horizon orientation mode is a specific string field/axion/B-field modulus, nor that trace-normalized Ford spectral weight is a physical string probability. No such identification was inserted.",
   "next_hard_gate":"Search the actual complex Kähler/string field content for the missing orientation-like degree and test whether its standard kinetic/Kähler structure supplies the 3/25 slot without modifying string theory."
 }
}
RESULTS.write_text(json.dumps(result,indent=2),encoding="utf-8")

print("="*96)
print("FORD–STRING BRIDGE v4 — DISTINGUISHABILITY SOLDERING")
print("="*96)
print("String no-scale identity:",no_scale)
print("String metric in (common,shape1,shape2):",Gq)
print()
print("Isolated real Kähler shape sector:")
print("  2*(11/25) =",R_kahler_shape_1)
print("  common fraction =",p_common_kahler)
print("  50/50 balance? NO")
print()
print("Exact deficit:")
print("  1 - 22/25 =",balance_deficit,"= Ford orientation eigenweight")
print()
print("Restore complete Ford horizon non-common sector:")
print("  22/25 + 3/25 =",R_complete_1)
print("  common fraction =",p_common_complete)
print("  distinguishability angle = pi/4")
print()
print("STRICT RESULT:")
print("  isolated Kähler closure: FAIL")
print("  complete-state structural closure: PASS")
print("  the exact missing amount is the omitted orientation sector, not a fitted correction.")
print("  physical identification of that orientation slot on the string side remains OPEN.")
print("Results:",RESULTS)
