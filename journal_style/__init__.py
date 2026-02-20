"""
journal_style
-------------
A reusable system for creating publication-ready matplotlib figures.

Mirrors the ggplot2 workflow described in:
https://jaquent.github.io/2026/02/creating-actually-publication-ready-figures-for-journals-using-ggplot2/

Key ideas:
  1. Define journal dimensions upfront (mm → inches)
  2. Set global rcParams once (font sizes, line widths, etc.)
  3. Use a helper to get correctly-sized Figure objects
  4. Export at the right DPI in PNG or SVG

Usage:
    from journal_style import set_journal_style, journal_figure

    set_journal_style()                        # call once at top of script
    fig, axes = journal_figure(ncols=4)        # get a properly-sized figure
    # ... plot on axes ...
    fig.savefig("output.svg", ...)             # export
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


# ---------------------------------------------------------------------------
# 1. Journal dimension constants (mm)
# ---------------------------------------------------------------------------

# Common journal full-page widths in mm
JOURNAL_WIDTHS_MM = {
    "elsevier_single": 90,    # single column
    "elsevier_full":   190,   # full width (≈177 mm usable)
    "science_single":  57,
    "science_full":    120,
    "cell_single":     85,
    "cell_full":       178,
    "nature_single":   89,
    "nature_full":     183,
}

MM_PER_INCH = 25.4

# Default colorblind-friendly palette (Wong, 2011 — Nature Methods 8, 441)
PALETTE = [
    "#0072B2",  # blue
    "#D55E00",  # vermillion
    "#009E73",  # bluish green
    "#CC79A7",  # reddish purple
    "#E69F00",  # orange
    "#56B4E9",  # sky blue
    "#F0E442",  # yellow
    "#000000",  # black
]


def mm_to_inches(mm: float) -> float:
    return mm / MM_PER_INCH


# ---------------------------------------------------------------------------
# 2. Global style setter — call this ONCE at the top of your script/notebook
# ---------------------------------------------------------------------------

def set_journal_style(
    base_font_size: float = 7.0,
    line_width: float = 0.5,
    tick_length: float = 2.5,
    color: str = "black",
    font_family: str = "sans-serif",
    palette: list[str] | None = None,
):
    """
    Sets matplotlib rcParams to publication-appropriate defaults.

    Parameters
    ----------
    base_font_size : float
        Base font size in points. 6–8 pt is typical for journals.
        All other text elements are scaled relative to this.
    line_width : float
        Default line width for axes, ticks, and geom lines.
    tick_length : float
        Length of axis ticks in points.
    color : str
        Default text/line color.
    font_family : str
        Font family. 'sans-serif' is safe; set to 'serif' for some journals.
    palette : list of str or None
        List of hex color strings for the default color cycle.
        If None, uses PALETTE (colorblind-friendly, Wong 2011).

    Example
    -------
    >>> set_journal_style(base_font_size=7, line_width=0.5)
    """
    if palette is None:
        palette = PALETTE

    params = {
        # --- Font ---
        "font.family":          font_family,
        "font.size":            base_font_size,
        "axes.titlesize":       base_font_size,
        "axes.labelsize":       base_font_size,
        "xtick.labelsize":      base_font_size * 0.9,
        "ytick.labelsize":      base_font_size * 0.9,
        "legend.fontsize":      base_font_size * 0.9,
        "legend.title_fontsize": base_font_size,

        # --- Line widths ---
        "axes.linewidth":       line_width,
        "grid.linewidth":       line_width * 0.75,
        "lines.linewidth":      line_width * 1.5,   # for line plots
        "patch.linewidth":      line_width,          # bar/box edges

        # --- Ticks ---
        "xtick.major.width":    line_width,
        "ytick.major.width":    line_width,
        "xtick.minor.width":    line_width * 0.75,
        "ytick.minor.width":    line_width * 0.75,
        "xtick.major.size":     tick_length,
        "ytick.major.size":     tick_length,
        "xtick.minor.size":     tick_length * 0.6,
        "ytick.minor.size":     tick_length * 0.6,
        "xtick.direction":      "out",
        "ytick.direction":      "out",

        # --- Markers/scatter ---
        "lines.markersize":     2.5,

        # --- Text color ---
        "text.color":           color,
        "axes.labelcolor":      color,
        "xtick.color":          color,
        "ytick.color":          color,

        # --- Color cycle ---
        "axes.prop_cycle":      mpl.cycler(color=palette),

        # --- Axes style ---
        "axes.spines.top":      False,   # clean look — remove top spine
        "axes.spines.right":    False,   # remove right spine

        # --- Legend ---
        "legend.frameon":       False,
        "legend.handlelength":  1.0,
        "legend.handleheight":  0.7,

        # --- Layout ---
        "figure.constrained_layout.use": True,   # auto-adjusts spacing

        # --- Saving ---
        "savefig.dpi":          600,
        "savefig.bbox":         "tight",
        "savefig.pad_inches":   0.01,
        "svg.fonttype":         "none",   # keeps text editable in Inkscape
    }

    mpl.rcParams.update(params)
    print(f"Journal style set: {base_font_size}pt font, {line_width}pt lines.")


# ---------------------------------------------------------------------------
# 3. Figure factory — creates a Figure at the right physical size
# ---------------------------------------------------------------------------

def journal_figure(
    width_mm: float = 178.0,
    aspect_ratio: float = 0.25,
    nrows: int = 1,
    ncols: int = 1,
    **subplot_kwargs,
) -> tuple[plt.Figure, np.ndarray]:
    """
    Creates a matplotlib Figure at a precise physical size for journal export.

    Parameters
    ----------
    width_mm : float
        Total figure width in mm. Use JOURNAL_WIDTHS_MM constants or a custom value.
    aspect_ratio : float
        height / width ratio. E.g., 0.25 for a wide 1×4 panel figure,
        1.0 for a square figure. Adjust to taste.
    nrows, ncols : int
        Number of subplot rows and columns.
    **subplot_kwargs :
        Passed directly to plt.subplots() (e.g., sharex=True).

    Returns
    -------
    fig : plt.Figure
    axes : np.ndarray of Axes (always 2D, shape [nrows, ncols])

    Example
    -------
    >>> fig, axes = journal_figure(width_mm=178, aspect_ratio=0.3, ncols=4)
    >>> fig.savefig("figure1.svg")
    """
    width_in  = mm_to_inches(width_mm)
    height_in = width_in * aspect_ratio

    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=(width_in, height_in),
        squeeze=False,   # always return 2D array of axes
        **subplot_kwargs,
    )
    return fig, axes


# ---------------------------------------------------------------------------
# 4. Export helper
# ---------------------------------------------------------------------------

def save_figure(
    fig: plt.Figure,
    path: str,
    dpi: int = 600,
    fmt: str | None = None,
) -> None:
    """
    Saves a figure with publication-appropriate settings.

    Parameters
    ----------
    fig : plt.Figure
    path : str
        Output path. Extension determines format unless `fmt` is set.
        Prefer .svg for vector output editable in Inkscape.
    dpi : int
        Resolution for raster formats (PNG, TIFF). Ignored for SVG.
    fmt : str or None
        Force format (e.g. 'svg', 'png', 'pdf', 'tiff').

    SVG tip
    -------
    SVG is preferred for journals — scalable, editable in Inkscape,
    and version-control friendly. Set rcParam `svg.fonttype = 'none'`
    (already done by set_journal_style) to keep text editable.
    """
    kwargs = dict(dpi=dpi, bbox_inches="tight")
    if fmt:
        kwargs["format"] = fmt
    fig.savefig(path, **kwargs)
    print(f"Saved: {path}")


# ---------------------------------------------------------------------------
# 5. Demo — runs when script is executed directly
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import pandas as pd
    from sklearn.datasets import load_iris

    # Load iris data
    iris = load_iris(as_frame=True)
    df = iris.frame
    df["species"] = df["target"].map(dict(enumerate(iris.target_names)))

    # Apply journal style globally
    set_journal_style(base_font_size=7, line_width=0.5)

    # Create a 1×4 figure at 178 mm wide (Elsevier full width)
    fig, axes = journal_figure(width_mm=178, aspect_ratio=0.28, ncols=4)

    ax1, ax2, ax3, ax4 = axes[0]

    # Panel 1: Sepal length density
    for i, (sp, grp) in enumerate(df.groupby("species")):
        ax1.hist(grp["sepal length (cm)"], bins=15, alpha=0.6,
                 color=PALETTE[i], density=True, label=sp)
    ax1.set_xlabel("Sepal length (cm)")
    ax1.set_ylabel("Density")
    ax1.set_title("Sepal length\ndistribution")

    # Panel 2: Sepal width density
    for i, (sp, grp) in enumerate(df.groupby("species")):
        ax2.hist(grp["sepal width (cm)"], bins=15, alpha=0.6,
                 color=PALETTE[i], density=True)
    ax2.set_xlabel("Sepal width (cm)")
    ax2.set_ylabel("Density")
    ax2.set_title("Sepal width\ndistribution")

    # Panel 3: Boxplot by species
    species_list = df["species"].unique()
    bp_data = [df[df["species"] == sp]["sepal length (cm)"].values
               for sp in species_list]
    bp = ax3.boxplot(bp_data, patch_artist=True, widths=0.5)
    for patch, color in zip(bp["boxes"], PALETTE):
        patch.set_facecolor(color)
    ax3.set_xticks(range(1, len(species_list) + 1))
    ax3.set_xticklabels(species_list, rotation=15, ha="right")
    ax3.set_xlabel("Species")
    ax3.set_ylabel("Sepal length (cm)")
    ax3.set_title("Sepal length\nby species")

    # Panel 4: Scatter
    for i, (sp, grp) in enumerate(df.groupby("species")):
        ax4.scatter(grp["sepal width (cm)"], grp["sepal length (cm)"],
                    color=PALETTE[i], label=sp, alpha=0.7)
    ax4.set_xlabel("Sepal width (cm)")
    ax4.set_ylabel("Sepal length (cm)")
    ax4.set_title("Sepal length\nby width")

    # Export as both SVG (vector, editable) and PNG (for quick preview)
    save_figure(fig, "journal_figure_demo.svg")
    save_figure(fig, "journal_figure_demo.png", dpi=600)

    plt.close(fig)
    print("Done.")
