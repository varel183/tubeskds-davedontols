"""Visualization functions for central dogma sequence analysis."""

from collections import Counter

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def _save_or_show(output_path):
    if output_path:
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
    else:
        plt.tight_layout()
        plt.show()


def plot_base_composition(base_count, output_path=None):
    """Create a bar chart for DNA base composition."""
    labels = list(base_count.keys())
    values = list(base_count.values())

    plt.figure(figsize=(7, 5))
    plt.bar(labels, values, color=["#4C78A8", "#F58518", "#54A24B", "#E45756"])
    plt.title("DNA Base Composition")
    plt.xlabel("Base")
    plt.ylabel("Count")
    _save_or_show(output_path)


def plot_codon_frequency(codon_count, output_path=None):
    """Create a bar chart for RNA codon frequency."""
    sorted_codons = dict(sorted(codon_count.items()))

    plt.figure(figsize=(12, 5))
    plt.bar(sorted_codons.keys(), sorted_codons.values(), color="#4C78A8")
    plt.title("RNA Codon Frequency")
    plt.xlabel("Codon")
    plt.ylabel("Count")
    plt.xticks(rotation=90)
    _save_or_show(output_path)


def plot_amino_acid_composition(protein_sequence, output_path=None):
    """Create a bar chart for amino acid composition."""
    amino_acid_count = dict(sorted(Counter(protein_sequence).items()))

    plt.figure(figsize=(8, 5))
    plt.bar(amino_acid_count.keys(), amino_acid_count.values(), color="#72B7B2")
    plt.title("Amino Acid Composition")
    plt.xlabel("Amino Acid")
    plt.ylabel("Count")
    _save_or_show(output_path)
