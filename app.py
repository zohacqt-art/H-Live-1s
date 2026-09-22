"""
Hydrogen Atom - Ground State (1s) Interactive Calculator
==========================================================
Streamlit app: wavefunction, normalization, radial probability density
and contour plot of |psi_100|^2 for the hydrogen atom ground state.

Run with:
    streamlit run app.py
"""

import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
import streamlit as st

# ----------------------------------------------------------------------
# Page setup
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Hydrogen 1s Wavefunction Calculator",
    page_icon="⚛️",
    layout="wide",
)

# Bohr radius is used in normalized (dimensionless) units: a0 = 1.
# All lengths below are expressed in multiples of a0.
A0 = 1.0


# ----------------------------------------------------------------------
# Physics — psi_100 (ground state) and derived quantities
# ----------------------------------------------------------------------
def psi_100(r, a0=A0):
    """Ground-state (1s) radial wavefunction, psi_100(r)."""
    return (1 / np.sqrt(np.pi)) * (1 / a0 ** 1.5) * np.exp(-r / a0)


def psi_100_sq(r, a0=A0):
    """Probability density |psi_100(r)|^2."""
    return psi_100(r, a0) ** 2


def radial_prob_density(r, a0=A0):
    """Radial probability density P(r) = 4*pi*r^2*|psi(r)|^2."""
    return 4 * np.pi * r ** 2 * psi_100_sq(r, a0)


def normalization_integral(a0=A0):
    """Numerically integrate P(r) over [0, inf) -> should equal 1."""
    integrand = lambda r: 4 * np.pi * r ** 2 * psi_100_sq(r, a0)
    value, error = integrate.quad(integrand, 0, np.inf)
    return value, error


# ----------------------------------------------------------------------
# Tabs
# ----------------------------------------------------------------------
st.title("⚛️ Hydrogen Atom — Ground State (1s) Calculator")

tab1, tab2, tab3 = st.tabs(["📚 Libraries & Equations", "💻 Code", "🔴 Live 1s"])

# ========================================================================
# TAB 1 — Libraries & Equations
# ========================================================================
with tab1:
    st.header("Libraries Used")
    st.markdown(
        """
| Library | Used for |
|---|---|
| **numpy** | array creation (`np.linspace`), elementwise math, meshgrids (`np.meshgrid`) for the contour plot |
| **scipy** (`scipy.integrate`) | `integrate.quad` — numerically evaluating the normalization integral |
| **matplotlib** | rendering the wavefunction curve, radial probability curve and 2D contour plot |
| **streamlit** | the interactive app shell — sliders/toggles and live re-rendering on every parameter change (replaces `ipywidgets`, which the original notebook version used for its `FloatSlider` / `Button` widgets) |
        """
    )

    st.header("Equations Used")

    st.markdown("**1. Ground-state (1s) wavefunction**")
    st.latex(r"\psi_{100}(r) = \frac{1}{\sqrt{\pi}} \, \frac{1}{a_0^{3/2}} \, e^{-r/a_0}")

    st.markdown("**2. Probability density**")
    st.latex(r"|\psi_{100}(r)|^2 = \psi_{100}(r)^2")

    st.markdown("**3. Radial probability density**")
    st.latex(r"P(r) = 4\pi r^2 \, |\psi_{100}(r)|^2")

    st.markdown("**4. Normalization condition**")
    st.latex(r"\int_0^{\infty} P(r)\, dr = \int_0^{\infty} 4\pi r^2 |\psi_{100}(r)|^2 \, dr = 1")

    st.markdown("**5. Contour plot (2D slice through the nucleus, x–z plane)**")
    st.latex(r"R = \sqrt{x^2 + z^2}, \qquad |\psi_{100}(R)|^2")

    st.info(
        "The Bohr radius is used in **normalized units**: $a_0 = 1$. "
        "All distances (r, x, z) in this calculator are therefore expressed "
        "as multiples of the Bohr radius rather than in meters."
    )

# ========================================================================
# TAB 2 — Code (slide 2 of the source presentation)
# ========================================================================
with tab2:
    st.header("Code")
    st.image(
        "assets/code_screenshot.png",
        
        use_container_width=True,
    )
    with st.expander("Show as selectable text"):
        with open(__file__, "r") as f:
            st.code(f.read(), language="python")

# ========================================================================
# TAB 3 — Live 1s calculator (interactive, recomputed on every change)
# ========================================================================
with tab3:
    st.header("Live 1s Wavefunction Calculator")
    st.caption("Every plot below recomputes live.")

    ctrl1, ctrl2, ctrl3 = st.columns(3)
    with ctrl1:
        r_max = st.slider(
            "Plot range, r_max (× a₀)", min_value=2.0, max_value=20.0, value=10.0, step=0.5
        )
    with ctrl2:
        resolution = st.slider(
            "Grid resolution", min_value=50, max_value=400, value=200, step=10
        )
    with ctrl3:
        show_radial = st.toggle("Show Radial Probability Density", value=False)

    # --- live computation, driven entirely by the controls above ---
    r = np.linspace(0, r_max * A0, resolution)
    psi_vals = psi_100(r, A0)
    norm_value, norm_error = normalization_integral(A0)

    m1, m2 = st.columns(2)
    m1.metric("∫ |ψ|² dV", f"{norm_value:.6f}")
    m2.metric("Integration error estimate", f"{norm_error:.2e}")
    if abs(norm_value - 1.0) < 1e-4:
        st.success("Wavefunction is normalized.")
    else:
        st.warning("Wavefunction is not normalized within tolerance.")

    plot_col1, plot_col2 = st.columns(2)

    # Wavefunction curve
    with plot_col1:
        st.subheader("Wavefunction ψ₁₀₀(r)")
        fig1, ax1 = plt.subplots(figsize=(5, 4))
        ax1.plot(r, psi_vals, color="#2563eb", linewidth=2)
        ax1.set_xlabel("r (a₀)")
        ax1.set_ylabel("ψ₁₀₀(r)")
        ax1.set_title("1s Wavefunction")
        ax1.grid(alpha=0.3)
        st.pyplot(fig1, clear_figure=True)

    # Contour plot
    with plot_col2:
        st.subheader("Contour Plot of |ψ|²")
        lim = r_max * A0
        grid_n = max(50, resolution // 2)
        x = np.linspace(-lim, lim, grid_n)
        z = np.linspace(-lim, lim, grid_n)
        X, Z = np.meshgrid(x, z)
        R = np.sqrt(X ** 2 + Z ** 2)
        PSI2 = psi_100_sq(R, A0)
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        cf = ax2.contourf(X, Z, PSI2, levels=50, cmap="inferno")
        ax2.set_xlabel("x (a₀)")
        ax2.set_ylabel("z (a₀)")
        ax2.set_title("|ψ₁₀₀|² Contour (x–z plane)")
        ax2.set_aspect("equal")
        fig2.colorbar(cf, ax=ax2, label="|ψ|²")
        st.pyplot(fig2, clear_figure=True)

    # Radial probability density — only on toggle
    if show_radial:
        st.subheader("Radial Probability Density P(r)")
        P = radial_prob_density(r, A0)
        fig3, ax3 = plt.subplots(figsize=(10, 4))
        ax3.plot(r, P, color="#dc2626", linewidth=2)
        ax3.axvline(A0, color="gray", linestyle="--", linewidth=1, label="r = a₀")
        ax3.set_xlabel("r (a₀)")
        ax3.set_ylabel("P(r) = 4πr²|ψ|²")
        ax3.set_title("Radial Probability Density")
        ax3.legend()
        ax3.grid(alpha=0.3)
        st.pyplot(fig3, clear_figure=True)
    else:
        st.caption("Turn on \"Show Radial Probability Density\" above to plot P(r).")
