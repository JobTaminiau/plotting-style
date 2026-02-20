"""
line_plot.py
------------
Time-series style line plot with mean +/- std shading, demonstrating:
  - Custom set_journal_style() parameters (font size, line width)
  - aspect_ratio control for landscape figures
  - Legend and fill_between for confidence bands

Produces: line_plot.svg, line_plot.png
"""

import numpy as np
from journal_style import set_journal_style, journal_figure, save_figure

# Customise style: slightly larger text and thicker lines
set_journal_style(base_font_size=8, line_width=0.7)

rng = np.random.default_rng(99)

# Simulate 3 experimental conditions, each with 20 replicates
time = np.linspace(0, 10, 100)
conditions = {
    "Control":    lambda t: 1.0 * np.exp(-0.15 * t),
    "Treatment A": lambda t: 1.0 * np.exp(-0.30 * t),
    "Treatment B": lambda t: 1.0 * np.exp(-0.05 * t) * np.cos(0.8 * t),
}
n_replicates = 20

# Landscape figure — wider than tall
fig, axes = journal_figure(width_mm=120, aspect_ratio=0.55)
ax = axes[0, 0]

colors = ["#4c72b0", "#dd8452", "#55a868"]

for (label, fn), color in zip(conditions.items(), colors):
    # Generate replicates
    replicates = np.array(
        [fn(time) + rng.normal(0, 0.08, len(time)) for _ in range(n_replicates)]
    )
    mean = replicates.mean(axis=0)
    std = replicates.std(axis=0)

    ax.plot(time, mean, label=label, color=color)
    ax.fill_between(time, mean - std, mean + std, alpha=0.2, color=color)

ax.set_xlabel("Time (s)")
ax.set_ylabel("Signal intensity (a.u.)")
ax.set_title("Simulated experimental time-series")
ax.legend()

save_figure(fig, "line_plot.svg")
save_figure(fig, "line_plot.png")
