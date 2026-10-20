#!/usr/bin/env python3
"""Run the full suite and write a one-page summary.

Supplementary material for:
  "The Mereotopological Capabilities of Top-Level Ontologies:
   A Survey from an Industrial Perspective" (Hasanzadeh & Ameri)

Runs the five runner scripts in order, records each verdict, and writes
results/summary.txt. Exits 0 only when every suite passes.

Usage:
  python3 runner/run_all.py [--corpora PATH]
"""
import argparse
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

SUITES = [
    ("run_probes.py",      True,  "OWL-RL entailment probes"),
    ("run_shacl.py",       True,  "gUFO SHACL validation probe"),
    ("check_axiom_ids.py", True,  "BFO cited-axiom resolution"),
    ("sumo_models.py",     False, "SUMO finite model searches"),
    ("inventory.py",       True,  "artifact inventories and absence checks"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpora", default=str(ROOT / "corpora"))
    args = ap.parse_args()

    lines = []
    failed = 0
    for script, takes_corpora, label in SUITES:
        cmd = [sys.executable, str(ROOT / "runner" / script)]
        if takes_corpora:
            cmd += ["--corpora", args.corpora]
        print(f"==== {script} " + "=" * max(0, 60 - len(script)))
        r = subprocess.run(cmd)
        verdict = "PASS" if r.returncode == 0 else "FAIL"
        failed += 1 if r.returncode != 0 else 0
        lines.append(f"{verdict}  {script:20s} {label}")
        print()

    summary = ("suite summary\n" + "\n".join(lines) +
               f"\n{len(SUITES) - failed}/{len(SUITES)} suites pass\n")
    print(summary)
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results" / "summary.txt").write_text(summary)
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
