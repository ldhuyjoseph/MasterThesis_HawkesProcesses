# Hawkes Stochastic Processes: Theory and Simulation

This repository contains the LaTeX source for the thesis:

**Hawkes Stochastic Processes: Theory and Simulation**  
Author: Duc Huy Lam

## Build

Compile with `pdflatex`:

```bash
pdflatex hawkes_thesis_cleaned.tex
pdflatex hawkes_thesis_cleaned.tex
```

The second compilation pass resolves cross-references and the table of contents.

## Notes

- The source uses a `report` document class.
- Main packages include `amsmath`, `amsthm`, `mathtools`, `newtxtext`, `newtxmath`, `algorithm`, `algpseudocode`, `graphicx`, `float`, and `hyperref`.
- Figure/PDF inclusions are wrapped with file-existence checks, so the source can still compile even if external images are not present.
