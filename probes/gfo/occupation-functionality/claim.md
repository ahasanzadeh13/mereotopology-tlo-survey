# gfo/occupation-functionality

Paper claim (Section 6.4.2): `occupies` (from `Presential` to `Space`) is
declared functional and its inverse `occupied_by` inverse-functional --
the same constraint stated twice: one space entity per occupant.
Multilocation is thereby forbidden in OWL, while co-location stays
admissible, so the coincidence the theory features is not contradicted at
this layer, only left without vocabulary.

Probe, both directions. Co-location: two presentials assert occupation of
one space entity; under the OWL-RL closure no identification may be
derived (`p1 sameAs p2` absent). Multilocation: one presential asserts
occupation of two space entities; the functionality of occupation must
identify them (`s1 sameAs s2` entailed).
