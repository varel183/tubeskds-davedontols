"""Biological analysis functions for central dogma sequence data."""

from __future__ import annotations

from collections import Counter
from typing import Any

from central_dogma.core import (
    clean_sequence,
    split_into_codons,
    transcribe_dna_to_rna,
    translate_rna_to_protein,
)

STOP_CODONS_DNA = frozenset({"TAA", "TAG", "TGA"})


def calculate_gc_content(dna_sequence: object) -> float:
    """Calculate GC content percentage for a DNA sequence."""
    normalized_sequence = clean_sequence(dna_sequence)
    if not normalized_sequence:
        return 0.0

    gc_count = normalized_sequence.count("G") + normalized_sequence.count("C")
    return round((gc_count / len(normalized_sequence)) * 100, 2)


def calculate_at_content(dna_sequence: object) -> float:
    """Calculate AT content percentage for a DNA sequence."""
    normalized_sequence = clean_sequence(dna_sequence)
    if not normalized_sequence:
        return 0.0

    at_count = normalized_sequence.count("A") + normalized_sequence.count("T")
    return round((at_count / len(normalized_sequence)) * 100, 2)


def count_bases(dna_sequence: object) -> dict[str, int]:
    """Count A, T, G, and C bases in a DNA sequence."""
    normalized_sequence = clean_sequence(dna_sequence)
    return {
        "A": normalized_sequence.count("A"),
        "T": normalized_sequence.count("T"),
        "G": normalized_sequence.count("G"),
        "C": normalized_sequence.count("C"),
    }


def count_codons(rna_sequence: object) -> dict[str, int]:
    """Count complete codons in an RNA sequence."""
    return dict(Counter(split_into_codons(rna_sequence)))


def detect_start_codon(dna_sequence: object) -> list[int]:
    """Return reading-frame positions where the DNA start codon ATG appears."""
    codons = split_into_codons(dna_sequence)
    return [index * 3 for index, codon in enumerate(codons) if codon == "ATG"]


def detect_stop_codons(dna_sequence: object) -> list[int]:
    """Return reading-frame positions where DNA stop codons appear."""
    codons = split_into_codons(dna_sequence)
    return [index * 3 for index, codon in enumerate(codons) if codon in STOP_CODONS_DNA]


def find_orfs(dna_sequence: object) -> list[dict[str, int | str]]:
    """Find simple open reading frames in the first reading frame."""
    codons = split_into_codons(dna_sequence)
    orfs: list[dict[str, int | str]] = []

    for start_index, codon in enumerate(codons):
        if codon != "ATG":
            continue

        for stop_index in range(start_index + 1, len(codons)):
            if codons[stop_index] in STOP_CODONS_DNA:
                start_position = start_index * 3
                stop_position = stop_index * 3
                end_position = stop_position + 3
                orfs.append(
                    {
                        "start": start_position,
                        "stop": stop_position,
                        "end": end_position,
                        "length": end_position - start_position,
                        "stop_codon": codons[stop_index],
                    }
                )
                break

    return orfs


def get_longest_orf(orfs: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Return the longest ORF dictionary, or None if no ORF exists."""
    if not orfs:
        return None
    return max(orfs, key=lambda item: item["length"])


def analyze_sequence(dna_sequence: object) -> dict[str, Any]:
    """Analyze one DNA sequence and return biological information."""
    normalized_sequence = clean_sequence(dna_sequence)
    rna_sequence = transcribe_dna_to_rna(normalized_sequence)
    protein_sequence = translate_rna_to_protein(rna_sequence)
    start_positions = detect_start_codon(normalized_sequence)
    stop_positions = detect_stop_codons(normalized_sequence)
    orfs = find_orfs(normalized_sequence)

    return {
        "dna_length": len(normalized_sequence),
        "gc_content": calculate_gc_content(normalized_sequence),
        "at_content": calculate_at_content(normalized_sequence),
        "base_count": count_bases(normalized_sequence),
        "codon_count": count_codons(rna_sequence),
        "start_codon_positions": start_positions,
        "stop_codon_positions": stop_positions,
        "start_codon_count": len(start_positions),
        "stop_codon_count": len(stop_positions),
        "amino_acid_count": dict(Counter(protein_sequence)),
        "orfs": orfs,
        "longest_orf": get_longest_orf(orfs),
    }
