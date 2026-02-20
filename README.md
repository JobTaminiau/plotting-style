# journal-style

Reusable matplotlib helpers for publication-ready figures.

## Installation

```bash
pip install git+https://github.com/JobTaminiau/journal-style.git@v1.0.0
```

Pin a specific version in `requirements.txt`:
```
journal-style @ git+https://github.com/JobTaminiau/journal-style.git@v1.0.0
```

Or in `pyproject.toml`:
```toml
[project]
dependencies = [
    "journal-style @ git+https://github.com/JobTaminiau/journal-style.git@v1.0.0",
]
```

## Usage

```python
from journal_style import set_journal_style, journal_figure, save_figure, JOURNAL_WIDTHS_MM

set_journal_style(base_font_size=7, line_width=0.5)

fig, axes = journal_figure(width_mm=178, aspect_ratio=0.28, ncols=4)
# ... plot on axes ...
save_figure(fig, "figure1.svg")
```

## Journal width constants

```python
JOURNAL_WIDTHS_MM = {
    "elsevier_single": 90,    # single column
    "elsevier_full":   190,   # full width
    "science_single":  57,
    "science_full":    120,
    "cell_single":     85,
    "cell_full":       178,
    "nature_single":   89,
    "nature_full":     183,
}
```
