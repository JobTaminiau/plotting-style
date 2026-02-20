"""
journal_widths.py
-----------------
Renders the same plot at several journal column widths from
JOURNAL_WIDTHS_MM so you can compare physical sizes side-by-side.

Produces one file per width, e.g.:
    journal_width_nature_single.svg
    journal_width_elsevier_single.svg
    journal_width_elsevier_full.svg
"""

import numpy as np
from journal_style import (
    JOURNAL_WIDTHS_MM,
    set_journal_style,
    journal_figure,
    save_figure,
)

set_journal_style()

# Synthetic data (shared across all figures)
rng = np.random.default_rng(7)
x = np.linspace(0, 6, 80)
y = np.sin(x) + rng.normal(0, 0.15, len(x))

# Subset of widths to demonstrate
widths_to_show = ["nature_single", "elsevier_single", "elsevier_full"]

for name in widths_to_show:
    width_mm = JOURNAL_WIDTHS_MM[name]
    fig, axes = journal_figure(width_mm=width_mm, aspect_ratio=0.6)
    ax = axes[0, 0]

    ax.plot(x, np.sin(x), label="True signal")
    ax.scatter(x, y, s=6, alpha=0.5, label="Noisy data")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title(f"{name}  ({width_mm} mm)")
    ax.legend()

    save_figure(fig, f"journal_width_{name}.svg")

print("Compare the SVG files to see how column width affects the figure.")
