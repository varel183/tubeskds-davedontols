"""Command-line interface for the central dogma analysis pipeline."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Sequence

from central_dogma.pipeline import PipelineConfig, run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run central dogma sequence analysis.")
    parser.add_argument(
        "--input",
        type=Path,
        default=PipelineConfig.input_path,
        help="Path to the input CSV file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PipelineConfig.output_dir,
        help="Directory where CSV and chart outputs are written.",
    )
    parser.add_argument(
        "--output-csv-name",
        default=PipelineConfig.output_csv_name,
        help="Name of the output CSV file.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging verbosity.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(level=args.log_level, format="%(levelname)s: %(message)s")

    config = PipelineConfig(
        input_path=args.input,
        output_dir=args.output_dir,
        output_csv_name=args.output_csv_name,
    )
    result_table = run_pipeline(config)

    print(
        "Analysis complete. "
        f"Processed {len(result_table)} valid sequences. "
        f"Results saved to {config.output_csv_path}"
    )
    return 0
