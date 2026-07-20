# VCF Filtering Pipeline for Viral Cleavage Analysis

This project filters Variant Call Format (VCF) files to retain high-confidence missense variants found in canonical proteins for further downstream analysis on viral cleavage interactions. 

## Pipeline Overview

The filtering pipeline consists of five sequential steps:

1. Allele Count (AC) Filter
Filters the VCF file by allele count, keeping only variants with an allele count (AC) greater than or equal to **10**.

2. Missense Filter
Removes all variants that are not annotated as **missense mutations**.

3. PASS Filter
Keeps only variants that passed all quality control metrics (entries with the `PASS` filter status).

4. Information Extraction
Extracts only the protein acession number, allele count, and mutation position and amino acid substitution. Which is required for downstream analysis:

5. Canonical Protein Filter
Uses a list of canonical protein accession numbers (found in the misc folder) to retain only variants corresponding to canonical proteins and removes all non-canonical protein entries.
