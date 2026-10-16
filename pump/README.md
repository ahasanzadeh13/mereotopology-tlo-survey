# The pump, five times

The running example of the paper (Section 3.3, Figure 2) encoded in each
system's shipped artifact vocabulary, resolving Table 5: R1, the
impeller's assembly parthood in the pump; R2, the impeller-housing joint.
Where a cell of Table 5 says "inexpressible," the file says so in a
comment at the point where the assertion would stand, and the
corresponding absence check appears in results/.

| file      | R1 mechanism                          | R2 |
|-----------|---------------------------------------|----|
| dolce.ttl | temporary parthood, reified           | inexpressible (no connection) |
| bfo.ttl   | continuant parthood, temporalized pair| inexpressible (no connection) |
| sumo.kif  | part, holdsDuring context             | meetsSpatially; reified joint (see probes/sumo) |
| gfo.ttl   | typed parthood suite                  | inexpressible (definable in theory, unshipped) |
| gufo.ttl  | isComponentOf, typed                  | inexpressible (no connection) |

Each RDF file parses against its pinned artifact; sumo.kif follows
Merge.kif surface syntax. The SUMO joint assertion is included
deliberately: it is well-formed and natively assertable, and
probes/sumo/joint-unsatisfiability shows that the axioms it triggers
admit no model -- the paper's point that "the pump SUMO can state is not
one its axioms can mean."
