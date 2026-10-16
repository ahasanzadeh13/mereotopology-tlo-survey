# dolce/sum-reification-projection

Paper claim (Section 6.1.2): "Atemporal sum-reifications project to binary
parthood by a chain axiom present in the module (inv(sumAddend1) o sumResult
subPropertyOf partOf, with its twin for the second addend)."

Probe: assert one `RRelSum` reification linking addends `a`, `b` and result
`s`; assert nothing mereological. Expected under the OWL-RL closure:
`a partOf s` and `b partOf s` -- the two chain axioms fire, so the
reification projects back to plain binary parthood.

Negative controls: `s partOf a` (no converse), `a partOf b`, and
`a overlaps b` must remain absent -- a shared whole is not a shared part,
and the projection adds exactly the parthood the chains state, nothing more.
