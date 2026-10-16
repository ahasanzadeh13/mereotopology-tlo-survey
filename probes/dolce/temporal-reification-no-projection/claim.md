# dolce/temporal-reification-no-projection

Paper claim (Section 6.1.2): "Temporal reifications project presence only:
a time-dependent relation is never compiled to a timeless binary, and a
complete reified parthood instance yields no mereological entailment at all."

Probe: assert one complete `RRelTempPart` reification -- part `x`, whole
`y`, time `t` -- and nothing else. Expected under the OWL-RL closure:
`x presentAt t` and `y presentAt t` (the presence chains on tempPart and
tempWhole fire), while `x partOf y`, `x properPartOf y`,
`x constantPartOf y`, and `x overlaps y` all remain absent. The boundary
between the two reification strategies is principled: sums project to
parthood, temporal relations project to presence and to nothing else.
