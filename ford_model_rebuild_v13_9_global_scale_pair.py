"""
FORD MODEL REBUILD v13.0 — TWO-TRACK FIRST-PRINCIPLES START
============================================================
Fresh derivation.  No old Ford hierarchy, Gamma values, seam weights, mass formulas, or
calibrations are imported.

Track A: architecture/history.
Track B: minimal algebra required by each architectural operation.
Ledger status is FORCED / NATURAL / HYPOTHETICAL.
"""
import itertools, math, json, hashlib
import numpy as np

LEDGER=[]
def record(step,architecture,algebra,status,reason):
    LEDGER.append(dict(step=step,architecture=architecture,algebra=algebra,status=status,reason=reason))

# STEP 0 — undivided carrier: one undistinguished state.
record(0,'undivided carrier / no distinction yet','one-state set','FORCED','No distinction means no internal state separation.')

# STEP 1 — one binary distinction has two complementary sides and an involution exchanging them.
C2=(1,-1)
record(1,'one two-sided distinction','C2 = {+1,-1}, d^2=1','NATURAL','A reversible two-sided cut/distinction is minimally represented by an involution.')

# STEP 2 — current architectural input: three distinct binary division channels.
# If independent, their joint state space is the direct product C2^3, with 8 states.
THREE_STATES=list(itertools.product(C2,repeat=3))
assert len(THREE_STATES)==8
record(2,'three distinct binary division channels','C2^3, 8 joint sign states','HYPOTHETICAL','The count 8 follows if the three architectural divisions are independent binary channels; independence is a model claim to retain visibly.')

# STEP 3 — three labelled channels have exactly three unordered pairwise seams and six orientations.
seams=[(0,1),(0,2),(1,2)]
directed=[(i,j) for i in range(3) for j in range(3) if i!=j]
assert len(seams)==3 and len(directed)==6
record(3,'pairwise relations among three labels: 12,13,23; each has two orientations','six directed matrix units E_ij (i != j)','FORCED','Three labels have 3 unordered pairs and 6 ordered transitions.')

# Build the six directed matrix units E_ij.
E={}
for i,j in directed:
    M=np.zeros((3,3),complex);M[i,j]=1;E[(i,j)]=M

# STEP 4 — closure of directed transitions under commutator generates diagonal differences.
# [E_ij,E_ji]=E_ii-E_jj.  Only two diagonal differences are independent after removing common trace.
H12=E[(0,1)]@E[(1,0)]-E[(1,0)]@E[(0,1)]
H23=E[(1,2)]@E[(2,1)]-E[(2,1)]@E[(1,2)]
assert np.allclose(H12,np.diag([1,-1,0]))
assert np.allclose(H23,np.diag([0,1,-1]))

# Verify the complex span of 6 off-diagonal Eij + 2 independent traceless diagonals has dimension 8.
basis=[E[p] for p in directed]+[H12,H23]
flat=np.column_stack([M.reshape(-1) for M in basis])
rank=int(np.linalg.matrix_rank(flat,tol=1e-12))
assert rank==8
# Every basis matrix is traceless.
assert all(abs(np.trace(M))<1e-12 for M in basis)
record(4,'close the six directed seam operations under composition/commutator and remove the common diagonal mode','sl(3,C) complex closure; compact Hermitian real form su(3), dimension 8','FORCED','Opposite seam orientations generate diagonal differences; three diagonal values have only two independent traceless differences, so 6+2=8. The matrix-unit commutator closes on traceless 3x3 matrices.')

# Standard Hermitian Gell-Mann basis generated from the same six seam directions + two state directions.
i=1j
GM=[
 np.array([[0,1,0],[1,0,0],[0,0,0]],complex),
 np.array([[0,-i,0],[i,0,0],[0,0,0]],complex),
 np.diag([1,-1,0]).astype(complex),
 np.array([[0,0,1],[0,0,0],[1,0,0]],complex),
 np.array([[0,0,-i],[0,0,0],[i,0,0]],complex),
 np.array([[0,0,0],[0,0,1],[0,1,0]],complex),
 np.array([[0,0,0],[0,0,-i],[0,i,0]],complex),
 np.diag([1,1,-2]).astype(complex)/math.sqrt(3),
]
assert max(abs(np.trace(GM[a]@GM[b])-2*(a==b)) for a in range(8) for b in range(8))<1e-12

# STEP 5 — traceless projection of the preceding 8 sign configurations into the two-dimensional state plane.
def traceless_state(s):
    s=np.asarray(s,float);return s-s.mean()
projected=[traceless_state(s) for s in THREE_STATES]
zero_count=int(sum(np.linalg.norm(x)<1e-12 for x in projected))
nonzero=[x for x in projected if np.linalg.norm(x)>1e-12]
assert zero_count==2 and len(nonzero)==6
assert max(abs(np.dot(x,x)-8/3) for x in nonzero)<1e-12
record(5,'remove the common component from each of the 8 three-channel sign states','orthogonal projection to x1+x2+x3=0: 2 zero states + 6 equal-radius nonzero states','FORCED','The common mode is orthogonal to the traceless state plane. Projection of the eight cube vertices leaves two uniform states at zero and six nonuniform states on one radius.')

print('='*118)
print('FORD MODEL REBUILD v13.0 — TWO TRACK START')
print('='*118)
for r in LEDGER:
    print(f"STEP {r['step']} [{r['status']}]\n  ARCH: {r['architecture']}\n  ALG : {r['algebra']}\n  WHY : {r['reason']}")
print('\nIndependent algebraic result: six oriented seams + closure generate an 8D traceless 3x3 algebra.')
print('This independently points to su(3); the previous model is not used in obtaining rank=',rank)
print('Eight sign states -> traceless projection: zero states=',zero_count,' nonzero equal-radius states=',len(nonzero))

frozen={'version':'13.0-two-track','legacy_mass_structure_used':False,'ledger':LEDGER,'su3_closure_rank':rank,
        'three_cut_states':8,'projected_zero_states':zero_count,'projected_nonzero_states':len(nonzero)}
h=hashlib.sha256(json.dumps(frozen,sort_keys=True,separators=(',',':')).encode()).hexdigest();print('freeze SHA256:',h)

# ================================================================================================
# v13.1 — ANALYZE THE DIAGONAL MODE REMOVED BY THE TRACELESS PROJECTION
# ================================================================================================
# Three diagonal state values decompose orthogonally into:
#   (i) two relative/traceless directions (Cartan of su(3));
#   (ii) one common direction proportional to the identity.
# The common direction must be recorded rather than silently discarded.
I3=np.eye(3,dtype=complex)
G0=math.sqrt(2/3)*I3   # normalized so Tr(G0 G0)=2, matching Gell-Mann normalization
assert abs(np.trace(G0@G0)-2)<1e-12
assert max(abs(np.trace(G0@g)) for g in GM)<1e-12
assert max(np.linalg.norm(G0@g-g@G0) for g in GM)<1e-12

# Full Hermitian basis rank: central common mode + 8 su(3) directions = 9.
full_basis=[G0]+GM
full_rank=int(np.linalg.matrix_rank(np.column_stack([M.reshape(-1) for M in full_basis]),tol=1e-12))
assert full_rank==9

# Decompose any diagonal d=(d1,d2,d3) into common + relative pieces.
def diagonal_decomposition(d):
    d=np.asarray(d,float)
    common=float(np.mean(d))
    relative=d-common*np.ones(3)
    return common,relative

# For the eight binary parent states, the common coordinate records exactly what the traceless
# projection erased.  It takes values +/-1 for uniform states and +/-1/3 for mixed states.
COMMON_HISTORY=[]
for s in THREE_STATES:
    common,relative=diagonal_decomposition(s)
    COMMON_HISTORY.append({'state':s,'common':common,'relative':relative})
common_values=sorted(set(round(x['common'],12) for x in COMMON_HISTORY))
assert np.allclose(common_values,[-1.0,-1/3,1/3,1.0])

record(6,'retain the diagonal component removed by traceless projection','central U(1) common mode plus su(3): u(3)=u(1) direct-sum su(3), dimension 9','FORCED','Three diagonal values contain two relative differences plus one common value. The common identity direction commutes with every internal transition and cannot be generated or changed by su(3) commutators.')

print('\n'+'='*118)
print('v13.1 — THE LEFTOVER DIAGONAL MODE')
print('='*118)
print('removed direction: G0 = sqrt(2/3) I3')
print('commutator with all 8 su(3) generators: exactly zero')
print('orthogonal to all 8 Gell-Mann generators: exactly yes')
print('full algebraic state space if retained: u(3) = u(1) + su(3), dimension',full_rank)
print('common values inherited from the 8 parent sign states:',common_values)
for x in COMMON_HISTORY:print(x['state'],'common=',x['common'],'relative=',x['relative'].tolist())
print('RESULT: the discarded piece is not another relative interaction channel. It is the unique global/common mode shared by all three labels.')
print('Internal su(3) dynamics cannot alter it because it is central. If the model has an overall scale/history variable, this is a mathematically natural place for it to live — but that physical identification is not yet assumed.')

# ================================================================================================
# v13.2 — RESIDUAL / LEFTOVER LEDGER
# ================================================================================================
# Rule for the fresh rebuild: whenever an operation removes, quotients, projects out, leaves a
# kernel/nullspace, common mode, trace component, or unmatched sector, preserve it explicitly.
# A residual is NOT declared physical merely because it exists; it is protected from accidental loss.
RESIDUAL_LEDGER=[
    {
        'origin_step':'three diagonal values -> traceless relative state',
        'operation':'orthogonal split into common + traceless components',
        'retained_main':'2D Cartan relative plane inside su(3)',
        'residual':'1D common identity direction G0=sqrt(2/3) I3',
        'algebraic_role':'central u(1) direction; commutes with su(3)',
        'parent_values':['+1','+1/3','-1/3','-1'],
        'physical_status':'UNRESOLVED — preserve; possible global/history/scale relevance not assumed',
        'disposition':'PROTECTED / CARRIED FORWARD'
    }
]

def preserve_residual(origin_step,operation,retained_main,residual,algebraic_role='UNRESOLVED',physical_status='UNRESOLVED'):
    item={'origin_step':origin_step,'operation':operation,'retained_main':retained_main,'residual':residual,
          'algebraic_role':algebraic_role,'physical_status':physical_status,'disposition':'PROTECTED / CARRIED FORWARD'}
    RESIDUAL_LEDGER.append(item);return item

print('\n'+'='*118)
print('v13.2 — PROTECTED RESIDUAL LEDGER')
print('='*118)
for item in RESIDUAL_LEDGER:
    print(item)
print('RULE: no remainder is silently deleted.  Every leftover is exposed, labelled unresolved, and carried forward until a later architectural operation explains or eliminates it.')

# ================================================================================================
# v13.3 — CUMULATIVE DATA-INTEGRITY / PROVENANCE CHAIN
# ================================================================================================
# Every child version must preserve the complete parent bytes as its exact prefix unless an
# intentional migration is explicitly documented.  This makes silent data loss detectable.
from pathlib import Path as _V133_Path
import hashlib as _V133_hashlib
PARENT_FILE='ford_model_rebuild_v13_2_residual_ledger.py'
PARENT_BYTE_LENGTH=10282
PARENT_SHA256='646f3eccd5205f4ac93b8179cab15d189b9c22cecd8bfaca218099bb44f51e91'
_this_bytes=_V133_Path(__file__).read_bytes()
_inherited_prefix=_this_bytes[:PARENT_BYTE_LENGTH]
INHERITED_SHA256=_V133_hashlib.sha256(_inherited_prefix).hexdigest()
assert INHERITED_SHA256==PARENT_SHA256, 'INTEGRITY FAILURE: inherited parent content changed or was lost'
PROVENANCE_CHAIN={
    'parent_file':PARENT_FILE,
    'parent_byte_length':PARENT_BYTE_LENGTH,
    'parent_sha256':PARENT_SHA256,
    'inherited_prefix_sha256':INHERITED_SHA256,
    'parent_preserved_byte_for_byte':True,
    'policy':'append-only by default; intentional supersession must be documented, never silently deleted'
}
print('\n'+'='*118)
print('v13.3 — DATA INTEGRITY')
print('='*118)
print(PROVENANCE_CHAIN)
print('PASS: complete v13.2 parent is present byte-for-byte at the start of this script.')

# ================================================================================================
# v13.4 — TWO TRACKS ADVANCE TO THE 48: FRAMEWORK + ALGEBRA
# ================================================================================================
# FRAMEWORK TRACK (literal spherical geometry)
# F0: unit sphere S^2.
# F1-F3: three mutually orthogonal great-circle cuts x=0,y=0,z=0 -> 8 spherical octants.
# Reordering boundaries x=y, x=z, y=z and their signed equivalents refine each octant into 3!=6
# ordering chambers.  Therefore the full B3 spherical Coxeter arrangement has 8*6=48 chambers.
FRAMEWORK_TIMELINE=[
    {'stage':'F0','object':'S^2','operation':'undivided spherical carrier','regions':1,'status':'MODEL INPUT: horizon/carrier'},
    {'stage':'F1','object':'S^2 cut by one great circle','operation':'first binary cut','regions':2,'status':'FORCED once cut chosen'},
    {'stage':'F2','object':'two orthogonal great circles','operation':'second independent orthogonal cut','regions':4,'status':'FORCED under orthogonality/independence'},
    {'stage':'F3','object':'three orthogonal great circles','operation':'third independent orthogonal cut','regions':8,'status':'FORCED under orthogonality/independence'},
    {'stage':'F4','object':'B3 spherical chamber complex','operation':'within each sign octant resolve all 3! coordinate orderings','regions':48,'status':'FORCED by including all label reorderings'},
]
assert FRAMEWORK_TIMELINE[-1]['regions']==8*math.factorial(3)==48

# Nine B3 reflection planes in R^3: 3 coordinate sign boundaries + 6 pair-order boundaries.
B3_MIRRORS=['x=0','y=0','z=0','x=y','x=-y','x=z','x=-z','y=z','y=-z']
assert len(B3_MIRRORS)==9

# ALGEBRA TRACK
# All six permutations of the three labels act by conjugation on the full u(3) basis.
PERMS3=list(itertools.permutations(range(3)))
U3_BASIS=[G0]+GM
U3_PERM_REPS=[]
for p in PERMS3:
    P=np.zeros((3,3),complex)
    for col,row in enumerate(p):P[row,col]=1
    R=np.zeros((9,9),float)
    for a,A in enumerate(U3_BASIS):
        X=P@A@P.conj().T
        for b,B in enumerate(U3_BASIS):R[b,a]=float(np.real(np.trace(B@X)/2))
    assert np.linalg.norm(R.T@R-np.eye(9))<1e-10
    # common G0 mode is fixed exactly by every reordering
    assert np.linalg.norm(R[:,0]-np.eye(9)[:,0])<1e-10
    U3_PERM_REPS.append({'perm':p,'R':R})

# Combine 8 sign configurations with 6 reorderings: full signed-permutation configuration layer.
FULL48=[{'signs':s,'perm':p} for s in THREE_STATES for p in PERMS3]
assert len(FULL48)==48

# The common mode is carried through unchanged by the S3 permutation track.
common_fixed_error=max(np.linalg.norm(x['R'][:,0]-np.eye(9)[:,0]) for x in U3_PERM_REPS)

record(7,'three original divisions are label-equivalent, so include all 3! reorderings','S3 permutation action by conjugation on full u(3)','NATURAL','If labels 1,2,3 have no intrinsic ordering, all six reorderings must be represented. The central common mode is fixed while relative directions are permuted/mixed.')
record(8,'combine 8 sign sectors with 6 label reorderings','B3 = C2^3 semidirect S3, 48 labelled configurations','FORCED','Signed permutations of three coordinates consist of 2^3 sign choices and 3! reorderings.')

print('\n'+'='*118)
print('v13.4 — FRAMEWORK TRACK')
print('='*118)
for x in FRAMEWORK_TIMELINE:print(x)
print('B3 mirror planes:',B3_MIRRORS)
print('framework count: 8 octants x 6 orderings = 48 spherical chambers')
print('\n'+'='*118)
print('v13.4 — ALGEBRA TRACK')
print('='*118)
print('S3 reorderings:',PERMS3)
print('full u(3) permutation representation dimension: 9')
print('common-mode fixed error:',common_fixed_error)
print('configuration count: 8 sign states x 6 permutations =',len(FULL48))
print('TRACK AGREEMENT: framework and algebra independently arrive at the same 48 signed/order configurations.')
print('NOTE: no tetrahedral identification is inserted here. If a tetrahedral stage belongs, it must be re-derived later from the framework rather than inherited from the previous model.')

# ================================================================================================
# v13.4 — INTEGRITY CHECK AGAINST v13.3
# ================================================================================================
V134_PARENT_FILE='ford_model_rebuild_v13_3_integrity_chain.py'
V134_PARENT_BYTE_LENGTH=11742
V134_PARENT_SHA256='717c93c79a9239ec2222720a5e6acb133f0235fd6267e6123e87b70219bf4a37'
_v134_bytes=_V133_Path(__file__).read_bytes()
V134_INHERITED_SHA256=_V133_hashlib.sha256(_v134_bytes[:V134_PARENT_BYTE_LENGTH]).hexdigest()
assert V134_INHERITED_SHA256==V134_PARENT_SHA256, 'INTEGRITY FAILURE: v13.3 parent content changed/lost'
print('\nv13.4 INTEGRITY PASS:',V134_INHERITED_SHA256)

# ================================================================================================
# v13.5 — WHERE DOES THE TETRAHEDRON ACTUALLY ENTER?
# ================================================================================================
# Fresh test, not inherited from the old model:
# 1) su(3) has root system A2: six roots in a 2D regular hexagon; Weyl group S3.
# 2) tetrahedral reflection symmetry is Coxeter A3: Weyl/reflection group S4, order 24.
# Therefore su(3) closure does NOT by itself force tetrahedral geometry.
# 3) The current first-principles architecture has four named roles:
#       Distinction, Boundary, Relationship, Interaction.
#    The minimal simplex carrying four affinely independent roles is a 3-simplex: a tetrahedron.
#    If the four roles are required to enter symmetrically/equidistantly, it is the regular tetrahedron.

FIRST_PRINCIPLE_ROLES=['Distinction','Boundary','Relationship','Interaction']
assert len(FIRST_PRINCIPLE_ROLES)==4
# canonical regular tetrahedron unit directions, centered at origin
TETRA=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],float)/math.sqrt(3)
assert np.linalg.norm(TETRA.sum(axis=0))<1e-12
_dots=TETRA@TETRA.T
assert max(abs(_dots[i,j]+1/3) for i in range(4) for j in range(4) if i!=j)<1e-12

TETRAHEDRON_LEDGER={
 'su3_geometry':'A2 root hexagon / Weyl S3 — does not force tetrahedron',
 'tetrahedral_geometry':'A3 / S4, distinct from su3(A2)',
 'fresh_architectural_source':'four first-principle roles -> minimal 3-simplex',
 'regularity_condition':'all four roles treated symmetrically/equidistantly',
 'status':'NATURAL framework realization of the four-role architecture; NOT derived from su(3)',
}
record(9,'four first-principle roles considered simultaneously','minimal simplex with four vertices = tetrahedron; regular if roles are symmetric','NATURAL','Four affinely independent roles require a 3-simplex for the minimal simplex representation. This is a framework statement, separate from the su(3)/A2 internal algebra.')

print('\n'+'='*118)
print('v13.5 — TETRAHEDRON PLACEMENT')
print('='*118)
print(TETRAHEDRON_LEDGER)
print('tetrahedron vertex dot products: off-diagonal = -1/3')
print('CORRECTION TO TIMELINE: tetrahedral framework belongs with the four-role first-principles layer, not as a consequence of su(3).')
print('The su(3) algebra track remains the independent three-label/seam closure and has A2 hexagonal root geometry.')

# v13.5 integrity against v13.4
V135_PARENT_BYTE_LENGTH=16500
V135_PARENT_SHA256='78a593ce7f4ef1e59fd0a50bd5b54bbadc56193b5fd9f39e9a2999c216848c26'
_v135_bytes=_V133_Path(__file__).read_bytes()
V135_INHERITED_SHA256=_V133_hashlib.sha256(_v135_bytes[:V135_PARENT_BYTE_LENGTH]).hexdigest()
assert V135_INHERITED_SHA256==V135_PARENT_SHA256, 'INTEGRITY FAILURE: v13.4 parent changed/lost'
print('v13.5 INTEGRITY PASS:',V135_INHERITED_SHA256)

# ================================================================================================
# v13.6 — FRAMEWORK/ALGEBRA BRIDGE INSIDE THE TETRAHEDRON
# ================================================================================================
# Use the semantic asymmetry already present in the first principles:
# Distinction is the access/apex role; Boundary, Relationship, Interaction are the three
# aspects of the distinguished thing.  On the tetrahedral framework this gives one apex D
# and an opposite triangular face (B,R,I).
ROLE_INDEX={'D':0,'B':1,'R':2,'I':3}
TETRA_EDGES=[('D','B'),('D','R'),('D','I'),('B','R'),('B','I'),('R','I')]
APEX_EDGES=[('D','B'),('D','R'),('D','I')]
INTERNAL_SEAMS=[('B','R'),('B','I'),('R','I')]
assert len(TETRA_EDGES)==6 and len(APEX_EDGES)==3 and len(INTERNAL_SEAMS)==3

# The internal face is an equilateral triangle in a regular tetrahedron.  Its three oriented
# edge differences give six vectors.  Center the B,R,I face coordinates in its own plane and
# verify those six directed edge vectors form an A2 root system (equal length, hexagonal directions).
# Use canonical equilateral-triangle coordinates.
tri=np.array([[1,0],[-0.5,math.sqrt(3)/2],[-0.5,-math.sqrt(3)/2]],float)
root_vectors=[]
for i in range(3):
    for j in range(3):
        if i!=j:root_vectors.append(tri[i]-tri[j])
root_vectors=np.array(root_vectors)
root_lengths=np.linalg.norm(root_vectors,axis=1)
assert np.max(abs(root_lengths-root_lengths[0]))<1e-12
angles=np.mod(np.arctan2(root_vectors[:,1],root_vectors[:,0]),2*math.pi)
angles=np.sort(angles)
angle_gaps=np.diff(np.r_[angles,angles[0]+2*math.pi])
assert np.max(abs(angle_gaps-math.pi/3))<1e-12

# Match the three unoriented internal seams to the three SU(3) pair labels.
TETRA_SU3_SEAM_MAP={
    'B-R':'12 -> lambda1,lambda2',
    'B-I':'13 -> lambda4,lambda5',
    'R-I':'23 -> lambda6,lambda7',
}

record(10,'tetrahedral framework with D as access apex and B,R,I as the internal triangular face','oriented edges of the BRI face form the six A2 roots / su(3) off-diagonal channels','NATURAL','The tetrahedron supplies a literal equilateral three-vertex internal face. Its three edges have six orientations, which form the A2 hexagonal root geometry independently obtained from su(3).')

print('\n'+'='*118)
print('v13.6 — TETRAHEDRON / SU(3) BRIDGE')
print('='*118)
print('tetrahedron edges:',TETRA_EDGES)
print('apex/access edges:',APEX_EDGES)
print('internal BRI seams:',INTERNAL_SEAMS)
print('six oriented internal-edge vectors form equal-length directions separated by 60 degrees: A2 hexagon')
print('seam map:',TETRA_SU3_SEAM_MAP)
print('TRACK AGREEMENT: framework BRI face -> 3 seams -> 6 orientations; algebra -> A2/su(3) -> 6 roots.')
print('STATUS: the bridge is NATURAL given the architectural distinction between apex D and the three internal roles; it is not inferred merely from matching the number six.')

# v13.6 integrity against v13.5
V136_PARENT_BYTE_LENGTH=19382
V136_PARENT_SHA256='ebcc01198bb37ffaf3b9a378b8e5f39e126efc5a0a1b157447a4d88c58e8f5c7'
_v136_bytes=_V133_Path(__file__).read_bytes()
V136_INHERITED_SHA256=_V133_hashlib.sha256(_v136_bytes[:V136_PARENT_BYTE_LENGTH]).hexdigest()
assert V136_INHERITED_SHA256==V136_PARENT_SHA256, 'INTEGRITY FAILURE: v13.5 parent changed/lost'
print('v13.6 INTEGRITY PASS:',V136_INHERITED_SHA256)

# ================================================================================================
# v13.7 — THE THREE APEX EDGES / COMMON MODE / SU(3) WEIGHT PLANE
# ================================================================================================
# Analyze the three framework edges D-B, D-R, D-I that were deliberately left unresolved.
D=TETRA[0]; BRI=TETRA[1:]
base_centroid=BRI.mean(axis=0)
# In a regular tetrahedron, the apex-to-opposite-face-centroid axis is parallel to D.
assert np.linalg.norm(base_centroid + D/3)<1e-12
common_axis=D/np.linalg.norm(D)
# Center the B,R,I face on its centroid.  These three vectors lie in the plane perpendicular
# to the common axis and form an equilateral weight triangle.
WEIGHTS=BRI-base_centroid
assert np.max(abs(WEIGHTS@common_axis))<1e-12
_weight_gram=WEIGHTS@WEIGHTS.T
assert max(abs(_weight_gram[i,i]-8/9) for i in range(3))<1e-12
assert max(abs(_weight_gram[i,j]+4/9) for i in range(3) for j in range(3) if i!=j)<1e-12
# Their six directed differences form the A2 root hexagon.
TETRA_ROOTS=np.array([WEIGHTS[i]-WEIGHTS[j] for i in range(3) for j in range(3) if i!=j])
assert max(abs(np.dot(r,r)-8/3) for r in TETRA_ROOTS)<1e-12
# Each apex edge decomposes into the SAME common-axis component plus one of the three weight directions.
APEX_DECOMP=[]
for label,V,w in zip(['B','R','I'],BRI,WEIGHTS):
    edge=V-D; coeff=float(edge@common_axis); planar=edge-coeff*common_axis
    assert np.linalg.norm(planar-w)<1e-12
    APEX_DECOMP.append({'edge':'D-'+label,'common_coefficient':coeff,'relative_weight':w})
assert max(abs(x['common_coefficient']+4/3) for x in APEX_DECOMP)<1e-12

record(11,'resolve the three previously-unexplained apex edges D-B,D-R,D-I','each apex edge = identical common-axis component + one of three SU(3) fundamental-weight directions','FORCED for the chosen regular tetrahedral coordinates','The opposite-face centroid separates the tetrahedron into a one-dimensional normal/common axis and a two-dimensional centered equilateral face. Differences of the three face weights are the six A2 roots.')

print('\n'+'='*118)
print('v13.7 — COMMON AXIS + WEIGHT PLANE')
print('='*118)
print('base centroid = -D/3:',base_centroid.tolist())
print('common/apex axis:',common_axis.tolist())
print('centered BRI weights:',WEIGHTS.tolist())
print('weight Gram matrix:',_weight_gram.tolist())
print('apex-edge decompositions:',APEX_DECOMP)
print('RESULT: the framework independently splits into 1 common direction + 2 relative directions.')
print('This geometrically mirrors the algebraic diagonal split u(1) + Cartan(su3).')
print('The three centered face points form the SU(3) fundamental weight triangle; their six directed differences form the A2 root hexagon.')
print('The previously protected common mode now has a direct framework counterpart: the tetrahedral apex-to-face-centroid axis. Physical interpretation remains unresolved.')

# v13.7 integrity against v13.6
V137_PARENT_BYTE_LENGTH=22736
V137_PARENT_SHA256='5f41f80a76309ae2cf0eef2f765807dc47bbbe344392407d685a971a60119fed'
_v137_bytes=_V133_Path(__file__).read_bytes()
V137_INHERITED_SHA256=_V133_hashlib.sha256(_v137_bytes[:V137_PARENT_BYTE_LENGTH]).hexdigest()
assert V137_INHERITED_SHA256==V137_PARENT_SHA256, 'INTEGRITY FAILURE: v13.6 parent changed/lost'
print('v13.7 INTEGRITY PASS:',V137_INHERITED_SHA256)

# ================================================================================================
# v13.8 — TRACE THE 4/3 COMMON COEFFICIENT ONE STEP BACK
# ================================================================================================
# Do not treat 4/3 as an unexplained new constant.  Restore an arbitrary tetrahedral circumradius R.
# Four symmetric vertex vectors v_i centered at zero satisfy sum v_i=0 and |v_i|=R.
# Hence for apex D, the centroid of the opposite face is C=-(1/3)D.
# The apex-to-face-centroid displacement is C-D=-(4/3)D, so its magnitude is 4R/3.
# The invariant content is the tetrahedral median/centroid 3:1 division; the absolute R remains free.

def tetra_common_geometry(R=1.0):
    D_R=R*common_axis
    C_R=-D_R/3.0
    displacement=C_R-D_R
    return {'R':R,'apex':D_R,'opposite_face_centroid':C_R,
            'apex_to_face_centroid':displacement,'height':float(np.linalg.norm(displacement)),
            'height_over_R':float(np.linalg.norm(displacement)/R)}

_tg=tetra_common_geometry(1.0)
assert abs(_tg['height_over_R']-4/3)<1e-12
# Centroid (origin) divides the median from apex to opposite-face centroid in 3:1 ratio:
# |D->0| : |0->C| = R : R/3 = 3:1.
TETRA_MEDIAN_RATIO=(3,1)

preserve_residual(
    origin_step='four symmetric first-principle vertices -> regular tetrahedral framework',
    operation='normalize tetrahedral circumradius while extracting dimensionless shape ratios',
    retained_main='dimensionless tetrahedral ratios: face-centroid=-D/3; median split 3:1; height/R=4/3',
    residual='overall circumradius R',
    algebraic_role='global multiplicative geometric scale; cancels from the dimensionless tetrahedral ratios',
    physical_status='UNRESOLVED — possible later scale carrier; do not set permanently to 1'
)

record(12,'trace the common apex coefficient back to the four-role tetrahedral closure','4/3 = tetrahedral median height divided by circumradius; underlying centroid ratio 3:1','FORCED','For four equal-radius symmetric vertices with zero centroid, the other three sum to -D, so their centroid is -D/3. No extra constant is introduced.')

print('\n'+'='*118)
print('v13.8 — ORIGIN OF 4/3')
print('='*118)
print('parent condition: four equal-radius symmetric vertices with sum zero')
print('opposite-face centroid = -D/3')
print('centroid divides tetrahedral median 3:1')
print('apex-to-opposite-face-centroid height = 4R/3')
print('therefore 4/3 is a dimensionless shape ratio, not an independently chosen scale')
print('PROTECTED LEFTOVER: overall tetrahedral circumradius R remains unresolved and is now in the residual ledger.')

# v13.8 integrity against v13.7
V138_PARENT_BYTE_LENGTH=26097
V138_PARENT_SHA256='254c79692e1140b0b4dbe95920bdc354e1a9cc045916465c88de72effdd6afb3'
_v138_bytes=_V133_Path(__file__).read_bytes()
V138_INHERITED_SHA256=_V133_hashlib.sha256(_v138_bytes[:V138_PARENT_BYTE_LENGTH]).hexdigest()
assert V138_INHERITED_SHA256==V138_PARENT_SHA256, 'INTEGRITY FAILURE: v13.7 parent changed/lost'
print('v13.8 INTEGRITY PASS:',V138_INHERITED_SHA256)

# ================================================================================================
# v13.9 — TRACE THE REMAINING GLOBAL SCALE ON BOTH TRACKS
# ================================================================================================
# FRAMEWORK: if the four first-principle vertices are directions/points on the spherical carrier,
# the tetrahedral circumradius is inherited directly from that carrier: R_tet = R_sphere.
# This transfers the unresolved scale backward; it does not determine it.

def framework_scale_from_carrier(R_sphere):
    return {'R_sphere':R_sphere,'R_tetrahedron':R_sphere,'tetra_height':4*R_sphere/3,
            'tetra_inradius':R_sphere/3}

# ALGEBRA: restore an arbitrary parent distinction amplitude A instead of silently fixing signs to +/-1.
# s_i=+/-A.  Projection and seam rates are linear in A, so the architecture fixes ratios but not A.
def algebra_parent_with_amplitude(signs,A):
    s=A*np.asarray(signs,float)
    common=float(np.mean(s));relative=s-common*np.ones(3)
    a=(relative[0]-relative[1])/2
    b=(relative[0]+relative[1]-2*relative[2])/(2*math.sqrt(3))
    rates={'12':2*a,'13':a+math.sqrt(3)*b,'23':-a+math.sqrt(3)*b}
    return {'A':A,'state':s,'common':common,'relative':relative,'a':a,'b':b,'rates':rates}

# Unit-amplitude formulas generalize exactly: uniform common +/-A; mixed common +/-A/3;
# nonzero Cartan radius^2 = (4/3)A^2; seam magnitudes {0,2A,2A}.
for signs in THREE_STATES:
    z=algebra_parent_with_amplitude(signs,2.5)
    if len(set(signs))==1:
        assert abs(abs(z['common'])-2.5)<1e-12
    else:
        assert abs(abs(z['common'])-2.5/3)<1e-12
        assert abs(z['a']**2+z['b']**2-(4/3)*2.5**2)<1e-12
        assert sorted(round(abs(x),12) for x in z['rates'].values())==[0.0,5.0,5.0]

preserve_residual(
    origin_step='spherical carrier -> regular tetrahedral four-role framework',
    operation='place the four role vertices on the carrier sphere',
    retained_main='all tetrahedral dimensionless ratios',
    residual='R_sphere = R_tetrahedron',
    algebraic_role='framework global length scale',
    physical_status='UNRESOLVED — inherited from carrier; not fixed by tetrahedral symmetry'
)
preserve_residual(
    origin_step='binary parent distinction states s_i=+/-A',
    operation='common/relative split and su(3) seam construction',
    retained_main='dimensionless sign pattern and relative ratios',
    residual='A, the common amplitude of the parent binary distinction',
    algebraic_role='global algebraic amplitude multiplying common, Cartan, and seam rates',
    physical_status='UNRESOLVED — do not identify with R or a physical energy until a cross-track rule derives it'
)

record(13,'trace global normalization backward on both tracks','framework leaves R_sphere; algebra leaves parent amplitude A','FORCED as a bookkeeping result','All derived tetrahedral and su(3) relations are homogeneous under global rescaling. The architecture fixes ratios while these two overall normalizations remain.')

print('\n'+'='*118)
print('v13.9 — GLOBAL SCALE PAIR')
print('='*118)
print('FRAMEWORK residual: R_tetrahedron = R_sphere if tetra vertices live on the carrier')
print('ALGEBRA residual: parent signs are really +/-A; all common/Cartan/root rates scale linearly with A')
print('No current step derives A from R_sphere or vice versa.')
print('PROTECTED CROSS-TRACK QUESTION: is there a later/earlier operation that relates the global geometric scale R to the global algebraic amplitude A?')

# v13.9 integrity against v13.8
V139_PARENT_BYTE_LENGTH=29171
V139_PARENT_SHA256='2775b046dfd106610a87236e27f1d2dfe86ec24642db0640928fb6a595d22980'
_v139_bytes=_V133_Path(__file__).read_bytes()
V139_INHERITED_SHA256=_V133_hashlib.sha256(_v139_bytes[:V139_PARENT_BYTE_LENGTH]).hexdigest()
assert V139_INHERITED_SHA256==V139_PARENT_SHA256, 'INTEGRITY FAILURE: v13.8 parent changed/lost'
print('v13.9 INTEGRITY PASS:',V139_INHERITED_SHA256)
