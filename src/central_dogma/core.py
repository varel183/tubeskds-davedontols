"""Core central dogma functions for DNA, RNA, and protein conversion."""

from __future__ import annotations

VALID_DNA_BASES = frozenset({"A", "T", "G", "C"})
VALID_RNA_BASES = frozenset({"A", "U", "G", "C"})

RNA_CODON_TABLE: dict[str, str] = {
    "UUU": "F",
    "UUC": "F",
    "UUA": "L",
    "UUG": "L",
    "UCU": "S",
    "UCC": "S",
    "UCA": "S",
    "UCG": "S",
    "UAU": "Y",
    "UAC": "Y",
    "UAA": "*",
    "UAG": "*",
    "UGU": "C",
    "UGC": "C",
    "UGA": "*",
    "UGG": "W",
    "CUU": "L",
    "CUC": "L",
    "CUA": "L",
    "CUG": "L",
    "CCU": "P",
    "CCC": "P",
    "CCA": "P",
    "CCG": "P",
    "CAU": "H",
    "CAC": "H",
    "CAA": "Q",
    "CAG": "Q",
    "CGU": "R",
    "CGC": "R",
    "CGA": "R",
    "CGG": "R",
    "AUU": "I",
    "AUC": "I",
    "AUA": "I",
    "AUG": "M",
    "ACU": "T",
    "ACC": "T",
    "ACA": "T",
    "ACG": "T",
    "AAU": "N",
    "AAC": "N",
    "AAA": "K",
    "AAG": "K",
    "AGU": "S",
    "AGC": "S",
    "AGA": "R",
    "AGG": "R",
    "GUU": "V",
    "GUC": "V",
    "GUA": "V",
    "GUG": "V",
    "GCU": "A",
    "GCC": "A",
    "GCA": "A",
    "GCG": "A",
    "GAU": "D",
    "GAC": "D",
    "GAA": "E",
    "GAG": "E",
    "GGU": "G",
    "GGC": "G",
    "GGA": "G",
    "GGG": "G",
}


def clean_sequence(sequence: object) -> str:
    """Return an uppercase sequence without whitespace."""
    return "".join(str(sequence).upper().split())


def validate_dna(sequence: object) -> bool:
    """Return True when a sequence contains only valid DNA bases."""
    dna_sequence = clean_sequence(sequence)
    return bool(dna_sequence) and set(dna_sequence).issubset(VALID_DNA_BASES)


def validate_rna(sequence: object) -> bool:
    """Return True when a sequence contains only valid RNA bases."""
    rna_sequence = clean_sequence(sequence)
    return bool(rna_sequence) and set(rna_sequence).issubset(VALID_RNA_BASES)


def transcribe_dna_to_rna(dna_sequence: object) -> str:
    """Convert DNA to RNA by replacing thymine with uracil."""
    normalized_sequence = clean_sequence(dna_sequence)
    if not validate_dna(normalized_sequence):
        raise ValueError("DNA sequence can only contain A, T, G, and C.")
    return normalized_sequence.replace("T", "U")


def split_into_codons(sequence: object) -> list[str]:
    """Split a DNA or RNA sequence into complete codons."""
    normalized_sequence = clean_sequence(sequence)
    return [
        normalized_sequence[index : index + 3]
        for index in range(0, len(normalized_sequence) - 2, 3)
    ]


def translate_rna_to_protein(rna_sequence: object) -> str:
    """Translate RNA into a protein sequence using the standard codon table."""
    normalized_sequence = clean_sequence(rna_sequence)
    if not validate_rna(normalized_sequence):
        raise ValueError("RNA sequence can only contain A, U, G, and C.")

    protein: list[str] = []
    for codon in split_into_codons(normalized_sequence):
        amino_acid = RNA_CODON_TABLE.get(codon)
        if amino_acid == "*":
            break
        if amino_acid:
            protein.append(amino_acid)

    return "".join(protein)
