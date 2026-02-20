"""
multi_panel.py
--------------
2x2 multi-panel figure demonstrating:
  - journal_figure(nrows=2, ncols=2) with subplot kwargs
  - 2D axes indexing: axes[row, col]
  - Panel labels (A, B, C, D)
  - Different plot types per panel

Produces: multi_panel.svg, multi_panel.png
"""

import numpy as np
from journal_style import set_journal_style, journal_figure, save_figure

set_journal_style()

rng = np.random.default_rng(0)

fig, axes = journal_figure(
    width_mm=178,       # Elsevier / Cell full width
    aspect_ratio=0.8,
    nrows=2,
    ncols=2,
)

# --- Panel A: scatter ---
ax = axes[0, 0]
x = rng.normal(0, 1, 80)
y = 0.6 * x + rng.normal(0, 0.5, 80)
ax.scatter(x, y, alpha=0.6)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("Scatter")

# --- Panel B: line plot ---
ax = axes[0, 1]
t = np.linspace(0, 4 * np.pi, 200)
ax.plot(t, np.sin(t), label="sin")
ax.plot(t, np.cos(t), label="cos")
ax.set_xlabel("t")
ax.set_ylabel("Amplitude")
ax.set_title("Line plot")
ax.legend()

# --- Panel C: histogram ---
ax = axes[1, 0]
data = rng.normal(5, 1.5, 300)
ax.hist(data, bins=20, alpha=0.7)
ax.set_xlabel("Value")
ax.set_ylabel("Count")
ax.set_title("Histogram")

# --- Panel D: bar chart ---
ax = axes[1, 1]
categories = ["A", "B", "C", "D", "E"]
values = rng.integers(3, 15, len(categories))
ax.bar(categories, values, alpha=0.7)
ax.set_xlabel("Category")
ax.set_ylabel("Value")
ax.set_title("Bar chart")

# Add panel labels (A, B, C, D) in the top-left of each panel
for idx, ax in enumerate(axes.flat):
    label = chr(ord("A") + idx)
    ax.text(
        -0.15, 1.05, label,
        transform=ax.transAxes,
        fontsize=10,
        fontweight="bold",
        va="bottom",
    )

save_figure(fig, "multi_panel.svg")
save_figure(fig, "multi_panel.png")
