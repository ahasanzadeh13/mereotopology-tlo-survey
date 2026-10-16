# Replication package

Supplementary material for:

> **The Mereotopological Capabilities of Top-Level Ontologies:
> A Survey from an Industrial Perspective**
> Ali Hasanzadeh and Farhad Ameri

Archived at DOI [10.5281/zenodo.23424995](https://doi.org/10.5281/zenodo.23424995).
Licensed CC BY 4.0 (see LICENSE).

This package holds the executed record behind the paper's computed
claims: the entailment and validation probes, the finite model searches,
the artifact inventories, and the five encodings of the running example.
Every result is relative to the six pinned corpora of the paper's
Table 2 and to no other version.

## Layout

    pins/      the six repositories and commits (manifest.tsv), and
               fetch_pins.sh, which clones them into corpora/ at the pins
    probes/    one directory per probe: the claim it supports (claim.md or
               axioms.md), the test assertion set, and the expected result
    pump/      the running example of Section 3.3 encoded in each
               artifact's own vocabulary (Table 5, executable form)
    cq/        the scenario competency questions of Section 3.1
    runner/    the scripts; no reasoner beyond OWL-RL and SHACL is used
    results/   the recorded outputs the paper cites

The fetch script materializes each working tree directly at its pin
(no checkout of any repository's current HEAD). One sumo fixture
directory, tests/TPTP/feener_CHAD_examples, is excluded from checkout:
its file names carry an NTFS ":Zone.Identifier" suffix and cannot
exist on a Windows filesystem. For that one clone the fetch script also
relaxes git's Windows path validation (core.protectNTFS), which would
otherwise reject those names at the index before the exclusion applies;
the pinned tree is audited and the five excluded fixtures are its only
NTFS-invalid names. The clone is complete -- the exclusion affects
working-tree materialization only -- and nothing the paper cites lies
in that directory. If a corpora/ subfolder is incomplete
(an interrupted fetch), delete that subfolder and re-run the script.

## Reproduction

    sh pins/fetch_pins.sh
    pip install -r runner/requirements.txt
    python3 runner/run_probes.py        # OWL-RL entailment probes
    python3 runner/run_shacl.py         # gUFO SHACL validation probe
    python3 runner/check_axiom_ids.py   # BFO cited-axiom resolution
    python3 runner/sumo_models.py       # SUMO finite model searches
    python3 runner/inventory.py         # declarations and absence checks

Every command exits 0 and prints PASS for each check; outputs are
written to results/ and should match the recorded files.

## Probe index

| probe | paper | method |
|---|---|---|
| dolce/sum-reification-projection | 6.1.2 | OWL-RL closure |
| dolce/temporal-reification-no-projection | 6.1.2 | OWL-RL closure |
| bfo/cited-axioms | 6.2 | corpus audit (CL) |
| sumo/joint-unsatisfiability | 6.3.2 | exhaustive finite search |
| sumo/sum-chain-forcing | 6.3.2, 7.1 | exhaustive finite search |
| gfo/occupation-functionality | 6.4.2 | OWL-RL closure |
| gufo/shacl-silence | 6.5.2 | SHACL validation |
| inventory (DOLCE, gUFO, GFO) | 6.1.2, 6.4.2, 6.5.2 | corpus audit |

## Scope of the checks

In the paper's own terms (Section 8.3), the machine checks are
consistency-grade. Three distinctions apply.

Executable here: the OWL-RL entailment probes, the SHACL probe, the
finite model searches, and the inventories -- everything in the table
above.

Audited, not re-proved: the paper's readings of BFO's Common Logic
axioms (e.g., the temporal-identity mechanism of Section 6.2) are
supported by the cited-axiom check, which verifies that every cited
axiom exists at the pin and reproduces its source comment; the
derivations themselves are the paper's, made against those axioms.

Documented only: claims about the SUMO translation pipelines (the
temporal wrapper surviving only as comments in the OWL exports) concern
external export tooling and are documented in the paper from the
published exports; no export generation is reproduced here.

## Tool versions

Python 3.11; exact library pins in runner/requirements.txt. The OWL-RL
closure is owlrl's OWL 2 RL implementation; SHACL validation is pySHACL;
no other reasoner is involved.
