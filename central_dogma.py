"""Core central dogma functions for DNA, RNA, and protein conversion."""

RNA_CODON_TABLE = {
    "UUU": "F", "UUC": "F", "UUA": "L", "UUG": "L",
    "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S",
    "UAU": "Y", "UAC": "Y", "UAA": "*", "UAG": "*",
    "UGU": "C", "UGC": "C", "UGA": "*", "UGG": "W",
    "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
    "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "CAU": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "AUU": "I", "AUC": "I", "AUA": "I", "AUG": "M",
    "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "AAU": "N", "AAC": "N", "AAA": "K", "AAG": "K",
    "AGU": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
    "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "GAU": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}


def clean_sequence(sequence):
    """Return an uppercase sequence without spaces or line breaks."""
    return "".join(str(sequence).upper().split())


def validate_dna(sequence):
    """Return True if sequence contains only valid DNA bases."""
    dna_sequence = clean_sequence(sequence)
    return bool(dna_sequence) and set(dna_sequence).issubset({"A", "T", "G", "C"})


def transcribe_dna_to_rna(dna_sequence):
    """Convert a DNA sequence to RNA by replacing T with U."""
    dna_sequence = clean_sequence(dna_sequence)
    if not validate_dna(dna_sequence):
        raise ValueError("DNA sequence can only contain A, T, G, and C.")
    return dna_sequence.replace("T", "U")


def split_into_codons(sequence):
    """Split a DNA or RNA sequence into complete codons."""
    sequence = clean_sequence(sequence)
    return [sequence[index:index + 3] for index in range(0, len(sequence) - 2, 3)]


def translate_rna_to_protein(rna_sequence):
    """Translate RNA into a protein sequence using the standard codon table."""
    rna_sequence = clean_sequence(rna_sequence)
    if not rna_sequence or not set(rna_sequence).issubset({"A", "U", "G", "C"}):
        raise ValueError("RNA sequence can only contain A, U, G, and C.")

    protein = []
    for codon in split_into_codons(rna_sequence):
        amino_acid = RNA_CODON_TABLE.get(codon)
        if amino_acid == "*":
            break
        if amino_acid:
            protein.append(amino_acid)

    return "".join(protein)
