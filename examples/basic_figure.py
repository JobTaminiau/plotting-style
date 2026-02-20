"""
basic_figure.py
---------------
Minimal example: the core 3-step workflow.

    1. set_journal_style()   — configure rcParams once
    2. journal_figure()      — create a correctly-sized figure
    3. save_figure()         — export at publication quality

Produces: basic_figure.svg, basic_figure.png
"""

import numpy as np
from journal_style import set_journal_style, journal_figure, save_figure

# Step 1 — apply journal defaults
set_journal_style()

# Synthetic data
rng = np.random.default_rng(42)
x = rng.uniform(0, 10, 60)
y = 2.5 * x + rng.normal(0, 3, 60)

# Step 2 — create a single-panel figure (Nature single-column width)
fig, axes = journal_figure(width_mm=89, aspect_ratio=0.8)
ax = axes[0, 0]

ax.scatter(x, y, alpha=0.7)
ax.set_xlabel("X variable")
ax.set_ylabel("Y variable")
ax.set_title("Basic scatter plot")

# Step 3 — save
save_figure(fig, "basic_figure.svg")
save_figure(fig, "basic_figure.png")
