#!/usr/bin/env python3
"""Independent extraction of tabular data from historical Andes virus PDFs.

This script intentionally avoids re‑using the existing `extract_historical_studies.py`
code. It uses the command‑line utility `pdftotext` (with the `-layout` flag) to
preserve column alignment, then parses each page's text looking for rows that
contain at least two columns separated by two or more spaces. Detected rows are
written to CSV files with a Unix‑timestamp suffix for cache‑busting.

The three PDFs reside in the `literature/` folder. The resulting CSV files are
saved in `data/`.
"""

import os
import subprocess
import time
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LIT_DIR = BASE_DIR / "literature"
DATA_DIR = BASE_DIR / "data"
TMP_DIR = BASE_DIR / "tmp_extraction"
TMP_DIR.mkdir(exist_ok=True)

PDF_MAP = {
    "martinez": "Martinez - human to human Andes virus - NEJM 2020.pdf",
    "padula": "Padula - human to human Andes virus - Virology 1998.pdf",
    "vial": "Vial - incubation period of Andes virus - EID 2006.pdf",
}

def timestamp() -> str:
    return str(int(time.time()))

def run_pdftotext(pdf_path: Path, out_txt: Path) -> None:
    """Run `pdftotext -layout` to preserve column spacing.
    The function raises an exception if the command fails.
    """
    cmd = ["pdftotext", "-layout", str(pdf_path), str(out_txt)]
    subprocess.run(cmd, check=True)

def parse_table_from_text(txt_path: Path) -> list:
    """Parse simple space‑separated tables from a txt file.

    Returns a list of rows, each row is a list of column strings.
    The heuristic: a line with at least two groups of non‑space characters
    separated by two or more spaces is considered a table row.
    """
    rows = []
    with txt_path.open(encoding="utf-8", errors="ignore") as f:
        for raw in f:
            # Strip trailing newlines but keep leading spaces for alignment
            line = raw.rstrip("\n")
            # Skip empty lines
            if not line.strip():
                continue
            # Heuristic: split on 2+ spaces
            parts = [p.strip() for p in line.split("  ") if p.strip()]
            if len(parts) >= 2:
                rows.append(parts)
    return rows

def save_rows_to_csv(rows: list, prefix: str, page_num: int) -> None:
    if not rows:
        return
    ts = timestamp()
    csv_name = f"{prefix}_page{page_num}_ind_{ts}.csv"
    out_path = DATA_DIR / csv_name
    # Determine max column count to pad shorter rows
    max_cols = max(len(r) for r in rows)
    with out_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for r in rows:
            padded = r + [""] * (max_cols - len(r))
            writer.writerow(padded)
    print(f"Saved independent table to {out_path}")

def extract_independent(pdf_key: str, pdf_name: str) -> None:
    pdf_path = LIT_DIR / pdf_name
    if not pdf_path.exists():
        print(f"⚠️ PDF not found: {pdf_path}")
        return
    # Convert entire PDF to a single txt (layout preserves columns across pages)
    txt_path = TMP_DIR / f"{pdf_key}.txt"
    try:
        run_pdftotext(pdf_path, txt_path)
    except subprocess.CalledProcessError as e:
        print(f"⚠️ pdftotext failed for {pdf_path}: {e}")
        return
    # Split txt into pages (pdftotext inserts a form‑feed character \f between pages)
    with txt_path.open(encoding="utf-8", errors="ignore") as f:
        content = f.read()
    pages = content.split("\f")
    for i, page_txt in enumerate(pages, start=1):
        # Write each page to a temporary file for parsing convenience
        page_file = TMP_DIR / f"{pdf_key}_page{i}.txt"
        page_file.write_text(page_txt, encoding="utf-8")
        rows = parse_table_from_text(page_file)
        if rows:
            save_rows_to_csv(rows, pdf_key, i)
        # Clean up temporary page file
        page_file.unlink(missing_ok=True)
    # Remove the combined txt file
    txt_path.unlink(missing_ok=True)

def main():
    for key, fname in PDF_MAP.items():
        print(f"🔎 Independently extracting tables from {fname}")
        extract_independent(key, fname)
    # Clean up tmp directory if empty
    try:
        TMP_DIR.rmdir()
    except OSError:
        pass

if __name__ == "__main__":
    main()
