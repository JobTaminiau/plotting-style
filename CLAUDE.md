# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`journal-style` is a single-module Python package providing matplotlib helpers for creating publication-ready figures. It wraps common rcParams configuration, figure sizing (in mm), and export into a simple API. The design mirrors a ggplot2 workflow for reproducible journal figures.

## Key Commands

```bash
# Run the demo (requires pandas and scikit-learn)
python -m journal_style

# Install as a package (editable, for development)
pip install -e .

# Install with demo dependencies
pip install -e ".[demo]"
```

There is no test suite, linter config, or build pipeline currently configured.

## Architecture

The entire library lives in `journal_style/__init__.py`. It exposes four public symbols:

- **`JOURNAL_WIDTHS_MM`** — dict of common journal column widths in mm (Elsevier, Nature, Science, Cell)
- **`set_journal_style()`** — sets matplotlib `rcParams` globally (font sizes, line widths, tick styling, spine removal, constrained layout, SVG text-as-text). Call once per script/notebook.
- **`journal_figure()`** — creates a `Figure` at an exact physical size (mm → inches) with a 2D axes array (never squeezed)
- **`save_figure()`** — saves with tight bbox and 600 DPI default; SVG preferred for editability

## Conventions

- All dimensions are specified in **millimeters**; conversion uses `MM_PER_INCH = 25.4`.
- `journal_figure()` always returns axes as a 2D `np.ndarray` (`squeeze=False`), so indexing is always `axes[row, col]`.
- Default style removes top and right spines, uses constrained layout, and sets `svg.fonttype = "none"` so text stays editable in Inkscape.
- The `__main__` block contains an Iris dataset demo producing SVG and PNG outputs.

## Packaging

The package is pip-installable via `pyproject.toml` with setuptools. The package name is `journal-style`, requires Python >=3.10, and depends on `matplotlib>=3.7` and `numpy>=1.24`.
