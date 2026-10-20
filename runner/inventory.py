#!/usr/bin/env python3
"""Artifact inventory and absence checks.

Supplementary material for:
  "The Mereotopological Capabilities of Top-Level Ontologies:
   A Survey from an Industrial Perspective" (Hasanzadeh & Ameri)

Scripted audits of what each pinned artifact declares (paper, Section
5.4): property chains, transitivity declarations, and the documented
absence checks behind the matrix's Silent cells. Each block states the
paper claim it supports and reports PASS/FAIL.

Usage:
  python3 runner/inventory.py [--corpora PATH]
"""
import argparse
import pathlib

import rdflib
from rdflib import OWL, RDF

ROOT = pathlib.Path(__file__).resolve().parent.parent
LINES = []
FAILURES = []


def log(s):
    print(s)
    LINES.append(s)


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


def check(name, condition):
    log(f"  {name}: {'PASS' if condition else 'FAIL'}")
    if not condition:
        FAILURES.append(name)


def local(uri):
    return str(uri).rsplit("#", 1)[-1].rsplit("/", 1)[-1]


def chains(g):
    """Return {property: [chain members]} for every owl:propertyChainAxiom."""
    out = {}
    for p, node in g.subject_objects(OWL.propertyChainAxiom):
        members = []
        while node and node != RDF.nil:
            first = g.value(node, RDF.first)
            inv = g.value(first, OWL.inverseOf) if isinstance(first, rdflib.BNode) else None
            members.append(f"inv({local(inv)})" if inv else local(first))
            node = g.value(node, RDF.rest)
        out.setdefault(local(p), []).append(members)
    return out


def transitive(g):
    return {local(s) for s in g.subjects(RDF.type, OWL.TransitiveProperty)}


def terms_matching(g, needles):
    hits = set()
    for s in set(g.subjects()):
        n = str(s).lower()
        if any(k in n for k in needles):
            hits.add(local(s))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpora", default=str(ROOT / "corpora"))
    args = ap.parse_args()
    corp = pathlib.Path(args.corpora)

    # ---- DOLCE (Section 6.1.2) --------------------------------------------
    log("inventory: DOLCE (DOLCEbasic + DOLCEnaryRel)")
    g = rdflib.Graph()
    parse_into(g, corp / "DOLCE/OWL/DOLCEbasic.owl")
    parse_into(g, corp / "DOLCE/OWL/DOLCEnaryRel.owl")
    ch, tr = chains(g), transitive(g)
    check("overlap defined by chain inv(partOf) o partOf",
          ["inv(partOf)", "partOf"] in ch.get("overlaps", []))
    check("sum chains owned by partOf (both addends)",
          sorted(ch.get("partOf", [])) == sorted(
              [["inv(sumAddend1)", "sumResult"], ["inv(sumAddend2)", "sumResult"]]))
    check("presence chains on presentAt (suite present)",
          len(ch.get("presentAt", [])) >= 10)
    check("transitivity on the parthood family",
          {"partOf", "properPartOf", "constantPartOf", "temporalPartOf"} <= tr)
    check("no connection or boundary vocabulary",
          not terms_matching(g, ("connect", "boundar")))
    check("no SWRL rules in the pinned release",
          not any("swrl" in str(p).lower() for p in set(g.predicates())))
    check("no SHACL shapes in the pinned release",
          not any("shacl" in str(x).lower()
                  for x in set(g.subjects()) | set(g.predicates())))

    # ---- gUFO (Section 6.5.2) ---------------------------------------------
    log("inventory: gUFO")
    g = rdflib.Graph()
    parse_into(g, corp / "gufo/gufo.ttl")
    tr = transitive(g)
    check("isSubCollectionOf and isSubQuantityOf declared transitive",
          {"isSubCollectionOf", "isSubQuantityOf"} <= tr)
    check("isComponentOf and isCollectionMemberOf left undeclared",
          not ({"isComponentOf", "isCollectionMemberOf"} & tr))
    check("no connection vocabulary",
          not terms_matching(g, ("connect",)))

    # ---- GFO (Section 6.4.2) ----------------------------------------------
    log("inventory: GFO (gfo-base)")
    g = rdflib.Graph()
    parse_into(g, corp / "GFO/modules/gfo-base.owl")
    boundaries = terms_matching(g, ("boundar",))
    check("typed boundary vocabulary present",
          len(boundaries) >= 3)
    check("no connection or coincidence relation",
          not terms_matching(g, ("connect", "coincid")))
    check("occupies functional / occupied_by inverse-functional",
          any(local(s) == "occupies" for s in g.subjects(RDF.type, OWL.FunctionalProperty))
          and any(local(s) == "occupied_by"
                  for s in g.subjects(RDF.type, OWL.InverseFunctionalProperty)))

    log(f"result: {'PASS' if not FAILURES else 'FAIL ' + str(FAILURES)}")
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "inventory.txt").write_text("\n".join(LINES) + "\n", encoding="utf-8", newline="\n")
    raise SystemExit(0 if not FAILURES else 1)


if __name__ == "__main__":
    main()
