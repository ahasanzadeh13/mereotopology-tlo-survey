#!/bin/sh
# Fetch the six pinned corpora at the exact commits evaluated in the paper
# (Table 2). The corpora are not redistributed here; each remains under its
# own upstream license. Every result in this appendix is relative to these
# commits and to no other version.
#
# Clones use --no-checkout and the working tree is materialized directly at
# the pin, so the state of each repository's current HEAD is irrelevant and
# re-running the script re-pins a corpus directory that already exists.
#
# The sumo repository contains test fixtures (TPTP examples) whose file
# names end in an NTFS ":Zone.Identifier" suffix; names containing a colon
# cannot exist on a Windows filesystem, so that one fixture directory is
# excluded from working-tree materialization via sparse-checkout, and
# git's Windows path validation (core.protectNTFS) is relaxed for that one
# clone so the pinned tree can be indexed at all -- the validation rejects
# such names at the index, before sparse-checkout is consulted. The pinned
# tree has been audited: the five excluded fixture files are its only
# NTFS-invalid names, and the sparse rule keeps them from ever being
# written. The clone itself is complete -- the full object store is
# present and verifiable -- and nothing the paper cites lies in the
# excluded directory.
set -eu
cd "$(dirname "$0")/.."
mkdir -p corpora
clone () { # name url commit [exclude-dir]
  if [ ! -d "corpora/$1" ]; then git clone --no-checkout "$2" "corpora/$1"; fi
  if [ "$#" -ge 4 ]; then
    git -C "corpora/$1" config core.sparseCheckout true
    mkdir -p "corpora/$1/.git/info"
    printf '/*\n!%s\n' "$4" > "corpora/$1/.git/info/sparse-checkout"
    # Windows git rejects colon-named paths when they enter the index,
    # even though the sparse rule above keeps them out of the working
    # tree. Relax the check for this one audited clone (see header).
    git -C "corpora/$1" config core.protectNTFS false
  fi
  git -C "corpora/$1" checkout --quiet --force "$3"
  echo "pinned  $1  $(git -C "corpora/$1" rev-parse --short HEAD)"
}
clone DOLCE     https://github.com/appliedontolab/DOLCE    0e059fd
clone BFO-2020  https://github.com/BFO-ontology/BFO-2020   dd89f4a
clone sumo      https://github.com/ontologyportal/sumo     b1af486 "/tests/TPTP/feener_CHAD_examples/"
clone GFO       https://github.com/Onto-Med/GFO            233b38d
clone gfo-light https://github.com/Onto-Med/gfo-light      1ca9d8d
clone gufo      https://github.com/nemo-ufes/gufo          f412254
