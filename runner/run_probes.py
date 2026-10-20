#!/usr/bin/env python3
"""Entailment-probe runner.

Supplementary material for:
  "The Mereotopological Capabilities of Top-Level Ontologies:
   A Survey from an Industrial Perspective" (Hasanzadeh & Ameri)

Protocol (paper, Sections 5.4 and 6): load the pinned artifact modules,
add a small test assertion set, compute the OWL-RL deductive closure, and
record (a) which of the expected entailments the reasoner actually draws
and (b) which statements remain absent. A probe passes when every
'expect_entailed' triple is present in the closure and every
'expect_absent' triple is not.

Each probe is a directory containing:
  probe.json      modules to load, prefixes, expected/absent triples
  assertions.ttl  the test assertion set
  claim.md        the paper claim the probe supports, with its section

Usage:
  python3 runner/run_probes.py [--corpora PATH] [probe-dir ...]
With no probe-dir arguments, every probes/*/*/probe.json is run.
"""
import argparse
import json
import pathlib
import sys

import rdflib
from rdflib.compare import to_canonical_graph
from owlrl import DeductiveClosure, OWLRL_Semantics

ROOT = pathlib.Path(__file__).resolve().parent.parent


def dump_closure(g, path):
    """Write the full closure as canonicalized, sorted N-Triples.

    Canonical blank-node labels plus sorted lines give the same bytes on
    every run and platform, so a re-run's dump is comparable (by diff or
    git) with the recorded one. The dump is the evidence behind the
    absence checks: grep it for a triple the probe expects absent and
    see for yourself that the reasoner did not draw it."""
    cg = to_canonical_graph(g)
    lines = sorted(cg.serialize(format="nt").splitlines())
    path.write_text("\n".join(lines) + "\n")


def parse_into(g, path):
    """Parse a local RDF file into g, portably. The file URI form matters:
    a bare Windows path (C:\\...) handed to rdflib is read as a URL whose
    scheme is the drive letter."""
    p = pathlib.Path(path).resolve()
    if not p.exists():
        raise SystemExit(f"missing file: {p}\n"
                         "Run pins/fetch_pins.sh first; if a corpora/ "
                         "subfolder exists but is incomplete, delete that "
                         "subfolder and run the fetch script again.")
    g.parse(p.as_uri())


def term(t, prefixes):
    """Expand a 'prefix:local' string to a URIRef using the probe's prefixes."""
    if not t.startswith("http") and ":" in t:
        prefix, local = t.split(":", 1)
        return rdflib.URIRef(prefixes[prefix] + local)
    return rdflib.URIRef(t)


def run_probe(probe_dir, corpora, closure_path):
    spec = json.loads((probe_dir / "probe.json").read_text())
    g = rdflib.Graph()
    for module in spec["modules"]:
        parse_into(g, corpora / module)
    parse_into(g, probe_dir / spec["assertions"])
    n_before = len(g)
    DeductiveClosure(OWLRL_Semantics).expand(g)
    dump_closure(g, closure_path)

    prefixes = spec.get("prefixes", {})
    lines = [f"probe: {spec['id']}",
             f"triples before/after closure: {n_before}/{len(g)}"]
    ok = True
    for s, p, o in spec.get("expect_entailed", []):
        present = (term(s, prefixes), term(p, prefixes), term(o, prefixes)) in g
        ok &= present
        lines.append(f"  entailed  {s} {p} {o}: {'PASS' if present else 'FAIL'}")
    for s, p, o in spec.get("expect_absent", []):
        present = (term(s, prefixes), term(p, prefixes), term(o, prefixes)) in g
        ok &= not present
        lines.append(f"  absent    {s} {p} {o}: {'PASS' if not present else 'FAIL'}")
    lines.append(f"closure written: results/closures/{closure_path.name}")
    lines.append(f"result: {'PASS' if ok else 'FAIL'}")
    return ok, "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpora", default=str(ROOT / "corpora"),
                    help="directory holding the pinned corpora (see pins/)")
    ap.add_argument("probes", nargs="*",
                    help="probe directories; default: all under probes/")
    args = ap.parse_args()
    corpora = pathlib.Path(args.corpora)

    if args.probes:
        probe_dirs = [pathlib.Path(p) for p in args.probes]
    else:
        probe_dirs = sorted(p.parent for p in ROOT.glob("probes/*/*/probe.json"))

    failures = 0
    outdir = ROOT / "results"
    outdir.mkdir(exist_ok=True)
    (outdir / "closures").mkdir(exist_ok=True)
    for probe_dir in probe_dirs:
        name = "_".join(probe_dir.parts[-2:])
        ok, report = run_probe(probe_dir, corpora,
                               outdir / "closures" / f"{name}.nt")
        print(report, "\n")
        (outdir / f"{name}.txt").write_text(report + "\n")
        failures += 0 if ok else 1
    print(f"{len(probe_dirs)} probe(s), {failures} failure(s)")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
