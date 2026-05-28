"""Visualization functions for central dogma sequence analysis."""

from __future__ import annotations

import os
import tempfile
from collections import Counter
from pathlib import Path

# Matplotlib and fontconfig read these paths during import.
if "MPLCONFIGDIR" not in os.environ:
    matplotlib_cache_dir = Path(tempfile.gettempdir()) / "central_dogma_matplotlib"
    matplotlib_cache_dir.mkdir(parents=True, exist_ok=True)
    os.environ["MPLCONFIGDIR"] = str(matplotlib_cache_dir)

if "XDG_CACHE_HOME" not in os.environ:
    xdg_cache_dir = Path(tempfile.gettempdir()) / "central_dogma_cache"
    xdg_cache_dir.mkdir(parents=True, exist_ok=True)
    os.environ["XDG_CACHE_HOME"] = str(xdg_cache_dir)

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def _save_or_show(figure: Figure, output_path: Path | str | None) -> None:
    figure.tight_layout()
    if output_path:
        figure.savefig(output_path, dpi=150)
        plt.close(figure)
        return

    plt.show()
    plt.close(figure)


def plot_base_composition(
    base_count: dict[str, int],
    output_path: Path | str | None = None,
) -> None:
    """Create a bar chart for DNA base composition."""
    labels = list(base_count.keys())
    values = list(base_count.values())

    figure, axis = plt.subplots(figsize=(7, 5))
    axis.bar(labels, values, color=["#4C78A8", "#F58518", "#54A24B", "#E45756"])
    axis.set_title("DNA Base Composition")
    axis.set_xlabel("Base")
    axis.set_ylabel("Count")
    _save_or_show(figure, output_path)


def plot_codon_frequency(
    codon_count: dict[str, int],
    output_path: Path | str | None = None,
) -> None:
    """Create a bar chart for RNA codon frequency."""
    sorted_codons = dict(sorted(codon_count.items()))

    figure, axis = plt.subplots(figsize=(12, 5))
    axis.bar(sorted_codons.keys(), sorted_codons.values(), color="#4C78A8")
    axis.set_title("RNA Codon Frequency")
    axis.set_xlabel("Codon")
    axis.set_ylabel("Count")
    axis.tick_params(axis="x", rotation=90)
    _save_or_show(figure, output_path)


def plot_amino_acid_composition(
    protein_sequence: str,
    output_path: Path | str | None = None,
) -> None:
    """Create a bar chart for amino acid composition."""
    amino_acid_count = dict(sorted(Counter(protein_sequence).items()))

    figure, axis = plt.subplots(figsize=(8, 5))
    axis.bar(amino_acid_count.keys(), amino_acid_count.values(), color="#72B7B2")
    axis.set_title("Amino Acid Composition")
    axis.set_xlabel("Amino Acid")
    axis.set_ylabel("Count")
    _save_or_show(figure, output_path)
