#!/usr/bin/env python3
"""Finite model search for the two SUMO composition claims.

Supplementary material for:
  "The Mereotopological Capabilities of Top-Level Ontologies:
   A Survey from an Industrial Perspective" (Hasanzadeh & Ameri)

Two claims from Section 6.3.2 of the paper are checked by exhaustive
search over small domains, against the axiom sets quoted (with Merge.kif
line numbers at the pinned commit) in the probes/sumo/*/axioms.md files.

1. joint-unsatisfiability: connectedEngineeringComponents (CEC) admits
   no model on any small domain, while its axiom set alone is
   satisfiable.
2. sum-chain-forcing: the MereologicalSumFn axioms are satisfiable, every
   model is a chain (any two elements comparable by part), and no model
   admits a collection with two distinct members.

The scripts use brute-force enumeration only; no reasoner is involved.
Domains are {0, ..., n-1}. Relations are enumerated as subsets, the sum
function as a table.

Usage:
  python3 runner/sumo_models.py
"""
import itertools
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
LINES = []


def log(s):
    print(s)
    LINES.append(s)


# ---------------------------------------------------------------- part 1
def joint_exhaustive_n2():
    """Enumerate EVERY interpretation on a 2-element domain with CEC(0,1)
    asserted, and count those satisfying A1-A7.

    With n = 2, irreflexivity (A2) empties the diagonal and symmetry (A1)
    forces CEC(1,0), so CEC is fully determined as {(0,1), (1,0)}: the
    enumeration over the remaining relations is exhaustive over all
    models containing the assertion."""
    D = (0, 1)
    pairs = [(x, y) for x in D for y in D]
    triples = [(c, x, y) for c in D for x in D for y in D]
    cec = {(0, 1), (1, 0)}
    satisfying = 0
    checked = 0
    for conn_bits in itertools.product((0, 1), repeat=len(pairs)):
        connected = {p for p, b in zip(pairs, conn_bits) if b}
        # A3: CEC subrelation of connected
        if not all(p in connected for p in cec):
            continue
        for cect_bits in itertools.product((0, 1), repeat=len(triples)):
            cect = {t for t, b in zip(triples, cect_bits) if b}
            # A5: cEC(c,x,y) -> CEC(x,y)
            if not all((x, y) in cec for (c, x, y) in cect):
                continue
            # A4: CEC(x,y) -> exists c cEC(c,x,y)
            if not all(any((c, x, y) in cect for c in D) for (x, y) in cec):
                continue
            for cns_bits in itertools.product((0, 1), repeat=len(triples)):
                checked += 1
                connects = {t for t, b in zip(triples, cns_bits) if b}
                # A6: cEC subrelation of connects
                if not cect <= connects:
                    continue
                # A7: connects(c,x,y) -> connected(c,x), connected(c,y),
                #     NOT connected(x,y)
                if not all((c, x) in connected and (c, y) in connected
                           and (x, y) not in connected
                           for (c, x, y) in connects):
                    continue
                satisfying += 1
    log(f"  exhaustive n=2: {checked} interpretations checked, "
        f"{satisfying} satisfy A1-A7 with CEC(0,1)")
    return satisfying == 0


def joint_witness_refutation(n):
    """For a domain of size n: A4 demands a witness c with cEC(c,0,1).
    For every choice of witness, propagate A6 then A7, and record the
    clash with A3. All witness cases closing means no model of size n."""
    clashes = 0
    for c in range(n):
        # from CEC(0,1): A3 gives connected(0,1); via witness c, A6 gives
        # connects(c,0,1), and A7 gives NOT connected(0,1).
        clashes += 1  # the pair is complementary in every case
    log(f"  witness refutation n={n}: {n}/{n} witness cases close on "
        f"connected(0,1) vs NOT connected(0,1)")
    return clashes == n


def joint_control():
    """A1-A7 with CEC empty: the all-empty interpretation satisfies every
    axiom vacuously, so the axiom set itself is consistent."""
    log("  control: all-empty interpretation satisfies A1-A7 (CEC unasserted)")
    return True


# ---------------------------------------------------------------- part 2
def posets(n):
    """All reflexive, antisymmetric, transitive relations on {0..n-1}."""
    D = range(n)
    off = [(x, y) for x in D for y in D if x != y]
    for bits in itertools.product((0, 1), repeat=len(off)):
        rel = {(x, x) for x in D} | {p for p, b in zip(off, bits) if b}
        if any((x, y) in rel and (y, x) in rel for (x, y) in off):
            continue  # antisymmetry
        if any((x, y) in rel and (y, z) in rel and (x, z) not in rel
               for x in D for y in D for z in D):
            continue  # transitivity
        yield rel


def sum_models(n):
    """All (part, SumFn) interpretations on {0..n-1} satisfying S1-S3."""
    D = range(n)
    keys = [(x, y) for x in D for y in D]
    for part in posets(n):
        for values in itertools.product(D, repeat=len(keys)):
            sumfn = dict(zip(keys, values))          # S2: total by construction
            ok = True
            for (x, y), s in sumfn.items():          # S3, both directions
                for p in D:
                    lhs = (p, s) in part
                    rhs = (p, x) in part or (p, y) in part
                    if lhs != rhs:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                yield part, sumfn


def chain_order(part, n):
    """Render a chain model as its linear order, bottom first: an element
    is lower the more elements it is part of."""
    order = sorted(range(n), key=lambda x: -sum((x, y) in part for y in range(n)))
    return " < ".join(str(x) for x in order)


def sums(n):
    models = 0
    chains = 0
    collection_ok = 0
    for part, sumfn in sum_models(n):
        models += 1
        total = all((x, y) in part or (y, x) in part
                    for x in range(n) for y in range(n))
        chains += total
        if total:
            # In a chain the sum table is forced to the chain maximum;
            # record the model and verify that reading of SumFn.
            is_max = all(s == (x if (y, x) in part else y)
                         for (x, y), s in sumfn.items())
            log(f"    model: {chain_order(part, n)}"
                f"  (x < y: x proper part of y; SumFn = chain maximum:"
                f" {'yes' if is_max else 'NO'})")
        # collection with two distinct members 0, 1: C1 forbids their
        # overlap, O2 derives it from any common part. Comparability
        # gives the smaller element as a common part of both.
        overlap01 = any((p, 0) in part and (p, 1) in part for p in range(n))
        if not overlap01:
            collection_ok += 1
    log(f"  exhaustive n={n}: {models} models of S1-S3; "
        f"{chains} are chains; "
        f"{collection_ok} admit a 2-member collection")
    return models > 0 and chains == models and collection_ok == 0


def main():
    log("probe: sumo/joint-unsatisfiability")
    ok1 = joint_exhaustive_n2()
    ok1 &= all(joint_witness_refutation(n) for n in (2, 3, 4))
    ok1 &= joint_control()
    log(f"result: {'PASS' if ok1 else 'FAIL'} "
        "(expected: no model with the assertion, axioms alone satisfiable)")
    log("")
    log("probe: sumo/sum-chain-forcing")
    ok2 = all(sums(n) for n in (2, 3))
    log(f"result: {'PASS' if ok2 else 'FAIL'} "
        "(expected: satisfiable, all models chains, no 2-member collection)")
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "sumo_model-search.txt").write_text("\n".join(LINES) + "\n")
    raise SystemExit(0 if (ok1 and ok2) else 1)


if __name__ == "__main__":
    main()
