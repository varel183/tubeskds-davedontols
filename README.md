# Pemodelan Komputasional Central Dogma

Analisis Terintegrasi DNA, RNA, dan Protein untuk Ekstraksi Informasi Biologis.

## Description

This project is a Python bioinformatics program that models the central dogma process:

```text
DNA -> RNA -> Protein
```

The program validates DNA sequences, transcribes DNA into RNA, translates RNA into protein, calculates biological statistics, exports results to CSV, and generates visualization charts.

## Research Focus

Research question:

```text
How can a simple Python-based computational model represent the central dogma process and extract biologically meaningful sequence features from DNA data?
```

Project contribution:

```text
This project provides an educational computational model that connects DNA validation, transcription, translation, GC/AT content, codon usage, amino acid composition, and open reading frame detection in one reproducible Python workflow.
```

## Features

1. DNA sequence validation.
2. DNA to RNA transcription.
3. RNA to protein translation using the standard codon table.
4. GC content calculation.
5. DNA base composition analysis.
6. RNA codon frequency analysis.
7. Start codon and stop codon detection.
8. AT content analysis.
9. Open reading frame detection.
10. Amino acid composition visualization.
11. CSV export for analysis results.

## Project Structure

```text
central-dogma-sequence-analysis/
|-- README.md
|-- requirements.txt
|-- main.py
|-- central_dogma.py
|-- analysis.py
|-- visualization.py
|-- data/
|   `-- sample_sequences.csv
|-- results/
|   `-- .gitkeep
|-- notebooks/
|   `-- central_dogma_demo.ipynb
`-- docs/
    `-- report_outline.md
```

## Installation

Create and activate a Python virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

Install the required Python packages inside the virtual environment:

```bash
pip install -r requirements.txt
```

## Usage

Run the main analysis pipeline:

```bash
python main.py
```

If the virtual environment is not activated, run the program directly with:

```bash
.\.venv\Scripts\python main.py
```

The program reads input data from:

```text
data/sample_sequences.csv
```

and writes output files to:

```text
results/
```

## Dataset

The current dataset contains synthetic educational DNA sequences designed to test different cases:

1. Normal coding sequences.
2. High GC and low GC sequences.
3. Multiple start codons.
4. Early stop codons.
5. No stop codon case.
6. One invalid sequence for validation testing.

For a stronger biological research submission, replace or extend `data/sample_sequences.csv` with real DNA sequences from a public database such as NCBI or Ensembl, then cite the data source in the report.

## Example Input

```csv
id,name,dna_sequence
SEQ001,Example coding sequence,ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG
```

## Example Output

The sequence above is transcribed and translated as:

```text
RNA: AUGGCCAUUGUAAUGGGCCGCUGAAAGGGUGCCCGAUAG
Protein: MAIVMGR
```

The generated CSV includes:

```text
id,name,dna_sequence,rna_sequence,protein_sequence,dna_length,gc_content,at_content,start_codon_count,stop_codon_count,orf_count,longest_orf_length
```

The generated visualization files are:

```text
results/analysis_results.csv
results/base_composition.png
results/codon_frequency.png
results/amino_acid_composition.png
```

## Contributors

Add your group members here:

1. Varel Tiara / 13523008
2. Bryan Ho / 13523029
3. Kenneth Poenadi / 13523040

## Submission Notes

Video presentation link:
