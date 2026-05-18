"""Biological analysis functions for central dogma sequence data."""

from collections import Counter

from central_dogma import split_into_codons, transcribe_dna_to_rna, translate_rna_to_protein

STOP_CODONS_DNA = {"TAA", "TAG", "TGA"}


def calculate_gc_content(dna_sequence):
    """Calculate GC content percentage for a DNA sequence."""
    dna_sequence = dna_sequence.upper()
    if len(dna_sequence) == 0:
        return 0.0

    gc_count = dna_sequence.count("G") + dna_sequence.count("C")
    return round((gc_count / len(dna_sequence)) * 100, 2)


def count_bases(dna_sequence):
    """Count A, T, G, and C bases in a DNA sequence."""
    dna_sequence = dna_sequence.upper()
    return {
        "A": dna_sequence.count("A"),
        "T": dna_sequence.count("T"),
        "G": dna_sequence.count("G"),
        "C": dna_sequence.count("C"),
    }


def count_codons(rna_sequence):
    """Count complete codons in an RNA sequence."""
    return dict(Counter(split_into_codons(rna_sequence)))


def calculate_at_content(dna_sequence):
    """Calculate AT content percentage for a DNA sequence."""
    dna_sequence = dna_sequence.upper()
    if len(dna_sequence) == 0:
        return 0.0

    at_count = dna_sequence.count("A") + dna_sequence.count("T")
    return round((at_count / len(dna_sequence)) * 100, 2)


def detect_start_codon(dna_sequence):
    """Return reading-frame positions where the DNA start codon ATG appears."""
    codons = split_into_codons(dna_sequence)
    return [index * 3 for index, codon in enumerate(codons) if codon == "ATG"]


def detect_stop_codons(dna_sequence):
    """Return reading-frame positions where DNA stop codons appear."""
    codons = split_into_codons(dna_sequence)
    return [index * 3 for index, codon in enumerate(codons) if codon in STOP_CODONS_DNA]


def find_orfs(dna_sequence):
    """Find simple open reading frames in the first reading frame."""
    dna_sequence = dna_sequence.upper()
    codons = split_into_codons(dna_sequence)
    orfs = []

    for start_index, codon in enumerate(codons):
        if codon != "ATG":
            continue

        for stop_index in range(start_index + 1, len(codons)):
            if codons[stop_index] in STOP_CODONS_DNA:
                start_position = start_index * 3
                stop_position = stop_index * 3
                end_position = stop_position + 3
                orfs.append({
                    "start": start_position,
                    "stop": stop_position,
                    "end": end_position,
                    "length": end_position - start_position,
                    "stop_codon": codons[stop_index],
                })
                break

    return orfs


def get_longest_orf(orfs):
    """Return the longest ORF dictionary, or None if no ORF exists."""
    if not orfs:
        return None
    return max(orfs, key=lambda item: item["length"])


def analyze_sequence(dna_sequence):
    """Analyze one DNA sequence and return biological information."""
    dna_sequence = dna_sequence.upper()
    rna_sequence = transcribe_dna_to_rna(dna_sequence)
    protein_sequence = translate_rna_to_protein(rna_sequence)
    start_positions = detect_start_codon(dna_sequence)
    stop_positions = detect_stop_codons(dna_sequence)
    orfs = find_orfs(dna_sequence)

    return {
        "dna_length": len(dna_sequence),
        "gc_content": calculate_gc_content(dna_sequence),
        "at_content": calculate_at_content(dna_sequence),
        "base_count": count_bases(dna_sequence),
        "codon_count": count_codons(rna_sequence),
        "start_codon_positions": start_positions,
        "stop_codon_positions": stop_positions,
        "start_codon_count": len(start_positions),
        "stop_codon_count": len(stop_positions),
        "amino_acid_count": dict(Counter(protein_sequence)),
        "orfs": orfs,
        "longest_orf": get_longest_orf(orfs),
    }
