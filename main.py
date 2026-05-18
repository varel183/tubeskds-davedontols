"""Main pipeline for the Central Dogma Sequence Analysis project."""

from collections import Counter
from pathlib import Path

import pandas as pd

from analysis import analyze_sequence
from central_dogma import clean_sequence, transcribe_dna_to_rna, translate_rna_to_protein, validate_dna
from visualization import plot_amino_acid_composition, plot_base_composition, plot_codon_frequency


DATA_PATH = Path("data/sample_sequences.csv")
RESULTS_DIR = Path("results")
OUTPUT_CSV = RESULTS_DIR / "analysis_results.csv"


def main():
    RESULTS_DIR.mkdir(exist_ok=True)

    sequences = pd.read_csv(DATA_PATH)
    analysis_rows = []
    combined_base_count = Counter()
    combined_codon_count = Counter()
    combined_protein = []

    for _, row in sequences.iterrows():
        dna_sequence = clean_sequence(row["dna_sequence"])

        if not validate_dna(dna_sequence):
            print(f"Skipping invalid DNA sequence: {row['id']} - {row['name']}")
            continue

        rna_sequence = transcribe_dna_to_rna(dna_sequence)
        protein_sequence = translate_rna_to_protein(rna_sequence)
        analysis = analyze_sequence(dna_sequence)
        longest_orf = analysis["longest_orf"] or {}

        combined_base_count.update(analysis["base_count"])
        combined_codon_count.update(analysis["codon_count"])
        combined_protein.append(protein_sequence)

        analysis_rows.append({
            "id": row["id"],
            "name": row["name"],
            "dna_sequence": dna_sequence,
            "rna_sequence": rna_sequence,
            "protein_sequence": protein_sequence,
            "dna_length": analysis["dna_length"],
            "gc_content": analysis["gc_content"],
            "at_content": analysis["at_content"],
            "start_codon_count": analysis["start_codon_count"],
            "stop_codon_count": analysis["stop_codon_count"],
            "start_codon_positions": analysis["start_codon_positions"],
            "stop_codon_positions": analysis["stop_codon_positions"],
            "orf_count": len(analysis["orfs"]),
            "longest_orf_start": longest_orf.get("start", ""),
            "longest_orf_end": longest_orf.get("end", ""),
            "longest_orf_length": longest_orf.get("length", 0),
            "longest_orf_stop_codon": longest_orf.get("stop_codon", ""),
        })

    result_table = pd.DataFrame(analysis_rows)
    result_table.to_csv(OUTPUT_CSV, index=False)

    if analysis_rows:
        plot_base_composition(dict(combined_base_count), RESULTS_DIR / "base_composition.png")
        plot_codon_frequency(dict(combined_codon_count), RESULTS_DIR / "codon_frequency.png")
        plot_amino_acid_composition("".join(combined_protein), RESULTS_DIR / "amino_acid_composition.png")

    print(f"Analysis complete. Results saved to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
