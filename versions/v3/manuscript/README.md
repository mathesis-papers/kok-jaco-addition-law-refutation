# The Jaco maximum-degree addition law

`note.tex` is the main source. It refutes Theorem 2.10 (Conjectured) of
arXiv:1404.0484v1 and gives the exact replacement, a proof of Lemma 2.2,
the requested page-11 partition, and corrections to Proposition 3.2.
The interval formula also supplies the missing order condition in Theorem 2.3,
the boundary in Proposition 2.8 and the corrected edge assertion in Theorem 2.15.
The addition formula extends to any number of summands, and the partition
formula extends to every arithmetic progression. These are extensions of
Patel's 2026 degree and cardinality solutions and Raso--Kok's independent
degree proof of 1 November 2026, cited in the note.
The historical comparison also identifies the original Fisher algorithm
and Bettina's theorem combined with the classical Hofstadter G identity
recorded by Rahman (2013) as earlier ingredients for the floor formula.
Conjecture 2.48.1 follows directly from Theorem 2.48 of Kok's 2016
journal account and the endpoint formula; the note makes this implication
explicit rather than presenting a new McPherson theorem.
The cited piecewise formula already appears in Kok--Susanth (2014),
Theorem 2.3, with the nonrepetition conjecture on the following page.
An exact three-maximizer recurrence reformulates Patel's prior classification for
Conjecture 2.16.1, including the artificial order-one seed. The full
maximum-set and never-singleton-label classifications are separate from
this addition-law note; Patel's identities are cited as tools.
`note.pdf` is the corresponding readable document.

## Build

Use Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively use a standard TeX distribution with the packages named in
`note.tex`, running `pdflatex note.tex` twice. The bibliography is embedded;
no external bibliography file, figure, or data file is needed.

## Finite checks

Python 3.10 or later, standard library only:

```sh
python3 verify.py > checker-output.json
```

The program constructs the graphs from their indegree recurrence without
using a golden-ratio formula in the construction. It compares all 131,328
degrees through order 512 with the closed formula, checks the indicated
addition pairs, 32,768 three-summand tuples, maximum-set intervals,
corrected local equivalences and arithmetic progressions, and writes the precise finite
domains and counterexample degree lists. All arithmetic is integral, including
the square-root floors. Compare the generated JSON with `checker-output.json`.
All exploding subsets and cliques are enumerated through order 12; clique
intervals are checked through order 512.

The addition-law corrections and extensions have written proofs in the note.
The indicated neighboring consequences use Patel's cited classification
and Kok's cited McPherson theorem with their hypotheses stated explicitly. At the pinned
revision linked in its final section, `JacoAdditionLawRefutation.result`
states the negation of the complete original conjecture, while
`JacoMaximumDegree.degree_formula` and `result` give the degree and maximum
formulas. The additional corrections have written proofs; the Python program
supplies the finite comparisons listed in its JSON output.
`JacoEndpointBeatty.endpoint_recurrence` and `endpoint_eq_beatty` supply the
recursive endpoint and floor connection at the same pinned revision.

## Contents and license

The source archive contains `note.tex`, `README.md`, `metadata.json`,
`verify.py`, and `checker-output.json`. The PDF is supplied separately.
Creators, in order: Haobo Ma (ChronoAI Pte Ltd, Singapore), then Wenlin Zhang
(National University of Singapore; ChronoAI Pte Ltd, Singapore).
License: Creative Commons Attribution 4.0 International (CC BY 4.0;
`cc-by-4.0`).
