# The pump, five times

The running example of the paper (Section 3.3, Figure 2) encoded in each
system's shipped artifact vocabulary, resolving Table 5: R1, the
impeller's assembly parthood in the pump; R2, the impeller-housing joint.
Where a cell of Table 5 says "inexpressible," the file says so in a
comment at the point where the assertion would stand, and the
corresponding absence check appears in results/inventory.txt.

| file      | R1 mechanism                                 | R2 |
|-----------|----------------------------------------------|----|
| dolce.ttl | temporary parthood, reified                  | inexpressible (no connection) |
| bfo.ttl   | continuant parthood, temporalized pair       | inexpressible (no connection) |
| sumo.kif  | part, holdsDuring context                    | meetsSpatially; reified joint (see probes/sumo) |
| gfo.ttl   | typed parthood suite (constituent_part_of)   | inexpressible (definable in theory, unshipped) |
| gufo.ttl  | isComponentOf, typed                         | inexpressible (no connection) |

Each RDF file parses against its pinned artifact; sumo.kif follows
Merge.kif surface syntax. The SUMO joint assertion is included
deliberately: it is well-formed and natively assertable, and
probes/sumo/joint-unsatisfiability shows that the axioms it triggers
admit no model -- the paper's point that "the pump SUMO can state is not
one its axioms can mean."

## Viewing the encodings

The files carry no owl:imports, because the corpora are not
redistributed: each encoding is written against the pinned clone that
pins/fetch_pins.sh fetches. So that a file still reads correctly when
opened on its own (in Protege, undeclared properties display as
annotation assertions), each file repeats the bare declarations -- class
and object-property typings -- of the artifact terms it uses. Nothing
more is repeated: property hierarchies, chain axioms, functionality and
transitivity live only in the pinned artifact, so no encoding can entail
anything the artifact does not supply.

To inspect an encoding with its full semantics, load it together with
its pinned module in one graph: in Python,

    import rdflib
    g = rdflib.Graph()
    g.parse("corpora/DOLCE/OWL/DOLCEbasic.owl")
    g.parse("corpora/DOLCE/OWL/DOLCEnaryRel.owl")
    g.parse("pump/dolce.ttl")

or, in Protege, open the pinned module from corpora/ and add an import
pointing at the encoding's local file (or merge the two once both are
open). The module each encoding expects is named in its header comment.
