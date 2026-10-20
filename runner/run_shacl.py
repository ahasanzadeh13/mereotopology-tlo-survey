#!/usr/bin/env python3
"""SHACL validation probe (gUFO).

Supplementary material for:
  "The Mereotopological Capabilities of Top-Level Ontologies:
   A Survey from an Industrial Perspective" (Hasanzadeh & Ameri)

Protocol (paper, Section 6.5.2): feed the gUFO SHACL companion a data
graph holding one type-side control violation and two mereological
errors (a supplementation violation and the banned member chain), and
record what the validator reports. The published claim is that the
control is flagged three times while both mereological errors pass in
silence.

Usage:
  python3 runner/run_shacl.py [--corpora PATH]
"""
import argparse
import pathlib

import rdflib
from pyshacl import validate

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROBE = ROOT / "probes" / "gufo" / "shacl-silence"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpora", default=str(ROOT / "corpora"))
    args = ap.parse_args()
    corpora = pathlib.Path(args.corpora)

    def parse_into(g, path):
        # file URI keeps the call portable: a bare Windows path (C:\...)
        # handed to rdflib is read as a URL whose scheme is the drive letter
        p = pathlib.Path(path).resolve()
        if not p.exists():
            raise SystemExit(f"missing file: {p}\n"
                             "Run pins/fetch_pins.sh first; if a corpora/ "
                             "subfolder exists but is incomplete, delete it "
                             "and run the fetch script again.")
        g.parse(p.as_uri())

    data = rdflib.Graph()
    parse_into(data, corpora / "gufo" / "gufo.ttl")
    parse_into(data, PROBE / "data.ttl")
    shapes = rdflib.Graph()
    parse_into(shapes, corpora / "gufo" / "examples" / "common" / "gufoshapes.ttl")

    conforms, report_graph, report_text = validate(
        data_graph=data, shacl_graph=shapes, inference="none")

    SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
    results = list(report_graph.subjects(rdflib.RDF.type, SH.ValidationResult))
    focus_nodes = [str(report_graph.value(r, SH.focusNode)) for r in results]

    mereo_terms = ("pump", "impeller", "blade", "member1", "fleet")
    mereo_hits = [f for f in focus_nodes if any(t in f for t in mereo_terms)]
    control_hits = [f for f in focus_nodes if "BadKind" in f]

    lines = ["probe: gufo/shacl-silence",
             f"conforms: {conforms}",
             f"violations reported: {len(results)}",
             f"violations on the type-side control (BadKind): {len(control_hits)}",
             f"violations on the mereological errors: {len(mereo_hits)}"]
    ok = (len(results) == 3 and len(control_hits) == 3 and len(mereo_hits) == 0)
    lines.append(f"result: {'PASS' if ok else 'FAIL'} "
                 "(expected: 3 violations, all on the control, none mereological)")
    report = "\n".join(lines)
    print(report)
    print()
    print(report_text)
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results" / "gufo_shacl-silence.txt").write_text(report + "\n", encoding="utf-8", newline="\n")
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
