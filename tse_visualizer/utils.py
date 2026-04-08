"""Utility helpers for text rendering and filesystem operations."""

from __future__ import annotations

from pathlib import Path

import arabic_reshaper
from bidi.algorithm import get_display
from matplotlib import font_manager as fm


DEFAULT_FONT_FALLBACK = "DejaVu Sans"


def reshape_persian_text(text: str) -> str:
    """Return bidirectional-safe text for Persian labels in matplotlib."""
    return get_display(arabic_reshaper.reshape(text))


def load_font(font_name: str = "Sahel.ttf") -> fm.FontProperties:
    """Load local Persian font if available; otherwise use a safe fallback font."""
    project_root = Path(__file__).resolve().parent.parent
    font_path = project_root / "fonts" / font_name

    if font_path.exists():
        fm.fontManager.addfont(str(font_path))
        return fm.FontProperties(fname=str(font_path))

    return fm.FontProperties(family=DEFAULT_FONT_FALLBACK)


def ensure_directory(path: str | Path) -> Path:
    """Create a directory if it does not exist and return a Path object."""
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory
