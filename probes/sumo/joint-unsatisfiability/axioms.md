# sumo/joint-unsatisfiability -- axiom set

Paper claim (Section 6.3.2): the engineering connection relation "is
unsatisfiable as axiomatized: it entails that its relata are connected,
while its mandatory connector entails, through the connects chain, that
they are not --- contradiction on first assertion, confirmed over all
small models."

The grounded axiom set, quoted from Merge.kif at pin b1af486 (line numbers
from that file). CEC abbreviates connectedEngineeringComponents; cEC
abbreviates connectsEngineeringComponents.

A1 (16536)  (instance connectedEngineeringComponents SymmetricRelation)
A2 (16537)  (instance connectedEngineeringComponents IrreflexiveRelation)
A3 (16539)  (subrelation connectedEngineeringComponents connected)
A4 (16591)  (=> (connectedEngineeringComponents ?COMP1 ?COMP2)
                (exists (?CONNECTION)
                  (connectsEngineeringComponents ?CONNECTION ?COMP1 ?COMP2)))
A5 (16596)  (=> (connectsEngineeringComponents ?CONNECTION ?COMP1 ?COMP2)
                (connectedEngineeringComponents ?COMP1 ?COMP2))
A6 (16600)  (subrelation connectsEngineeringComponents connects)
A7 (9827)   (=> (connects ?OBJ1 ?OBJ2 ?OBJ3)
                (and (connected ?OBJ1 ?OBJ2)
                     (connected ?OBJ1 ?OBJ3)
                     (not (connected ?OBJ2 ?OBJ3))))

The derivation of the contradiction, for arbitrary domains:
CEC(a,b) gives connected(a,b) by A3; A4 supplies a connector c with
cEC(c,a,b); A6 lifts it to connects(c,a,b); A7's third conjunct gives
NOT connected(a,b). Both conjuncts follow from the single assertion, so
no model of A1-A7 satisfies CEC(a,b) for any a, b.

The runner confirms this two ways: by exhaustive enumeration of every
interpretation on a two-element domain, and by the witness-case
refutation above instantiated on domains of size 2, 3, and 4. It also
confirms the control: A1-A7 alone (no CEC assertion) are satisfiable.
