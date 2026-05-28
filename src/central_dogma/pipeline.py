"""Pipeline orchestration for central dogma sequence analysis."""

from __future__ import annotations

import logging
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from central_dogma.analysis import analyze_sequence
from central_dogma.core import (
    clean_sequence,
    transcribe_dna_to_rna,
    translate_rna_to_protein,
    validate_dna,
)
from central_dogma.visualization import (
    plot_amino_acid_composition,
    plot_base_composition,
    plot_codon_frequency,
)

LOGGER = logging.getLogger(__name__)

REQUIRED_COLUMNS = frozenset({"id", "name", "dna_sequence"})
RESULT_COLUMNS = [
    "id",
    "name",
    "dna_sequence",
    "rna_sequence",
    "protein_sequence",
    "dna_length",
    "gc_content",
    "at_content",
    "start_codon_count",
    "stop_codon_count",
    "start_codon_positions",
    "stop_codon_positions",
    "orf_count",
    "longest_orf_start",
    "longest_orf_end",
    "longest_orf_length",
    "longest_orf_stop_codon",
]


@dataclass(frozen=True)
class PipelineConfig:
    """Configuration for one pipeline run."""

    input_path: Path = Path("data/sample_sequences.csv")
    output_dir: Path = Path("results")
    output_csv_name: str = "analysis_results.csv"

    @property
    def output_csv_path(self) -> Path:
        return self.output_dir / self.output_csv_name


def _validate_input_columns(dataframe: pd.DataFrame) -> None:
    missing_columns = REQUIRED_COLUMNS.difference(dataframe.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Input CSV is missing required columns: {missing}")


def _build_result_row(
    row: pd.Series,
    dna_sequence: str,
    analysis: dict[str, Any],
) -> dict[str, Any]:
    longest_orf = analysis["longest_orf"] or {}
    rna_sequence = transcribe_dna_to_rna(dna_sequence)
    protein_sequence = translate_rna_to_protein(rna_sequence)

    return {
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
    }


def run_pipeline(config: PipelineConfig | None = None) -> pd.DataFrame:
    """Run the full analysis workflow and return the generated result table."""
    config = config or PipelineConfig()
    config.output_dir.mkdir(parents=True, exist_ok=True)

    sequences = pd.read_csv(config.input_path)
    _validate_input_columns(sequences)

    analysis_rows: list[dict[str, Any]] = []
    combined_base_count: Counter[str] = Counter()
    combined_codon_count: Counter[str] = Counter()
    combined_protein: list[str] = []

    for _, row in sequences.iterrows():
        dna_sequence = clean_sequence(row["dna_sequence"])

        if not validate_dna(dna_sequence):
            LOGGER.warning(
                "Skipping invalid DNA sequence: %s - %s",
                row["id"],
                row["name"],
            )
            continue

        analysis = analyze_sequence(dna_sequence)
        analysis_rows.append(_build_result_row(row, dna_sequence, analysis))

        combined_base_count.update(analysis["base_count"])
        combined_codon_count.update(analysis["codon_count"])
        combined_protein.append(
            translate_rna_to_protein(transcribe_dna_to_rna(dna_sequence))
        )

    result_table = pd.DataFrame(analysis_rows, columns=RESULT_COLUMNS)
    result_table.to_csv(config.output_csv_path, index=False)

    if analysis_rows:
        plot_base_composition(
            dict(combined_base_count),
            config.output_dir / "base_composition.png",
        )
        plot_codon_frequency(dict(combined_codon_count), config.output_dir / "codon_frequency.png")
        plot_amino_acid_composition(
            "".join(combined_protein),
            config.output_dir / "amino_acid_composition.png",
        )

    return result_table
