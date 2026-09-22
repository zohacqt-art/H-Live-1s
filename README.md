# Hydrogen Atom — Ground State (1s) Interactive Calculator

Interactive Streamlit app for the hydrogen 1s wavefunction: ψ₁₀₀, |ψ|² normalization,
radial probability density, and a 2D contour plot — all recomputed live as you move
the controls.

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually http://localhost:8501).

## Tabs

1. **Libraries & Equations** — libraries used (numpy, scipy, matplotlib, streamlit)
   and the physics equations behind the calculator (wavefunction, probability
   density, radial probability density, normalization, contour-plot radius).
2. **Code** — a screenshot of the actual `app.py` powering this calculator
   (not the presentation slide), plus the same code as selectable text.
3. **Live 1s** — the working calculator. Adjust the plot range, grid resolution,
   or toggle the radial probability density on/off; the wavefunction curve,
   contour plot, and (when toggled) radial probability plot re-render live.

The Bohr radius is used in normalized units throughout (a₀ = 1); all distances
are expressed as multiples of a₀.
