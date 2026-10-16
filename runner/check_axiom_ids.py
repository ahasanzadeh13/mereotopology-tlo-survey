#!/usr/bin/env python3
"""Axiom-citation check (BFO-2020 Common Logic).

Supplementary material for:
  "The Mereotopological Capabilities of Top-Level Ontologies:
   A Survey from an Industrial Perspective" (Hasanzadeh & Ameri)

The paper cites BFO-2020 axioms by the corpus's own bracketed ids,
e.g. [tab-1]. This check verifies that every cited id resolves in the
Common Logic files at the pinned commit, and reproduces each axiom's
source comment so the paper's reading can be compared side by side
with the axiom it cites.

Usage:
  python3 runner/check_axiom_ids.py [--corpora PATH]
"""
import argparse
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
IDS = ROOT / "probes" / "bfo" / "cited-axioms" / "ids.txt"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpora", default=str(ROOT / "corpora"))
    args = ap.parse_args()
    cl_dir = pathlib.Path(args.corpora) / "BFO-2020" / "21838-2" / "common-logic"
    if not cl_dir.is_dir():
        raise SystemExit(f"missing directory: {cl_dir.resolve()}\n"
                         "Run pins/fetch_pins.sh first; if a corpora/ "
                         "subfolder exists but is incomplete, delete that "
                         "subfolder and run the fetch script again.")

    ids = [ln.strip() for ln in IDS.read_text().splitlines()
           if ln.strip() and not ln.startswith("#")]

    # Index every bracketed axiom id in the CL corpus, with the comment
    # text that precedes it. The corpus writes "comment '...' [id]" and
    # escapes apostrophes inside comments as \' -- the pattern below
    # steps over escaped characters. Some axioms are stated verbatim in
    # more than one module file; identical texts under one id count as
    # one axiom and both locations are reported.
    index = {}
    for cl_file in sorted(cl_dir.glob("*.cl")):
        text = cl_file.read_text(errors="replace")
        for m in re.finditer(r"cl:comment\s+'((?:[^'\\]|\\.)*)\[([a-z]{3}-\d)\]", text):
            index.setdefault(m.group(2), []).append(
                (cl_file.name, " ".join(m.group(1).split())))

    lines = ["probe: bfo/cited-axioms",
             f"ids cited in the paper: {len(ids)}"]
    ok = True
    for i in ids:
        hits = index.get(i, [])
        texts = {comment for _, comment in hits}
        if len(hits) >= 1 and len(texts) == 1:
            files = "; ".join(sorted({f for f, _ in hits}))
            note = "" if len(hits) == 1 else f" (stated in {len(hits)} files)"
            lines.append(f"  [{i}] PASS  {files}{note}: {hits[0][1]}")
        else:
            ok = False
            lines.append(f"  [{i}] FAIL  ({len(hits)} matches, "
                         f"{len(texts)} distinct texts)")
    lines.append(f"result: {'PASS' if ok else 'FAIL'}")
    report = "\n".join(lines)
    print(report)
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results" / "bfo_cited-axioms.txt").write_text(report + "\n")
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
