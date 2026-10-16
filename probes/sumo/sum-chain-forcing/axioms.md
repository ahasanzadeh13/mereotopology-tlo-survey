# sumo/sum-chain-forcing -- axiom set

Paper claim (Section 6.3.2): the composition functions are "total binary
functions over objects, defined by unguarded biconditionals," and these
axioms "force every model to be a chain: any two objects become
comparable by parthood." Re-derived "by exhaustive finite search and an
analytic argument." The defect propagates: "combined with the axiom that
distinct members of a Collection do not overlap, any collection with two
object members is contradictory."

The grounded axiom set, quoted from Merge.kif at pin b1af486:

S1 (918)    (instance part PartialOrderingRelation)
            [reflexive, antisymmetric, transitive]
S2 (10067)  (instance MereologicalSumFn TotalValuedRelation)
            [the sum of any two objects exists]
S3 (10079)  (=> (equal ?OBJ3 (MereologicalSumFn ?OBJ1 ?OBJ2))
                (forall (?PART)
                  (<=> (part ?PART ?OBJ3)
                       (or (part ?PART ?OBJ1) (part ?PART ?OBJ2)))))
O1 (9861)   (=> (overlapsSpatially ?OBJ1 ?OBJ2)
                (exists (?OBJ3)
                  (and (part ?OBJ3 ?OBJ1) (part ?OBJ3 ?OBJ2))))
O2 (9868)   (=> (and (part ?OBJ3 ?OBJ1) (part ?OBJ3 ?OBJ2))
                (overlapsSpatially ?OBJ1 ?OBJ2))
C1 (9873)   (=> (and (member ?OBJ1 ?COLL) (member ?OBJ2 ?COLL)
                     (not (equal ?OBJ1 ?OBJ2)))
                (not (overlapsSpatially ?OBJ1 ?OBJ2)))

The analytic argument (arbitrary domains). Let s = SumFn(x, y), which S2
guarantees to exist. By S1, part(s, s); by S3 read left to right at
?PART = s, part(s, x) or part(s, y). By S1 and S3 read right to left,
part(x, s) and part(y, s). In the first case antisymmetry gives s = x,
hence part(y, x); in the second, s = y, hence part(x, y). Either way x
and y are comparable: every model is a chain. For the propagation: two
distinct members a, b of a collection are comparable, say part(a, b);
with part(a, a) the pair has the common part a, so O2 gives
overlapsSpatially(a, b), contradicting C1.

The runner confirms this by exhaustive finite search: every
interpretation of (part, SumFn) on domains of size 2 and 3 satisfying
S1-S3 is enumerated; the theory is satisfiable, every model is a chain,
and no model extends to a collection with two distinct members.
