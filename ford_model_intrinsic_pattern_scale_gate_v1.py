# Ford Model intrinsic pattern-scale gate v1
# Reproduces the exact calculation reported in chat.
from fractions import Fraction
import math
lc=Fraction(1,1); ls=Fraction(11,128); lo=Fraction(3,128); Q=Fraction(1,4)
print("common, shape, orientation =", lc, ls, lo)
print("orientation/shape per cycle =", lo/ls)
print("orientation/shape power per cycle =", (lo/ls)**2)
for n in range(7):
    s=ls**n; o=lo**n
    rho=math.sqrt(float(s*s+o*o))
    print(n, "shape", s, "orientation", o, "rho", rho)
print("VERDICT: the existing map supplies a pattern-defined relative scale rho,")
print("but not yet an automatic clear->unclear->clear re-expression cycle.")
