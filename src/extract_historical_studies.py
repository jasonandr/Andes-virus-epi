#!/usr/bin/env python3
"""Extract tables from historical Andes virus study PDFs into CSV files.

This script uses pdfplumber to iterate over each page of the target PDFs and
extract any tabular data found. Each extracted table is saved as a CSV file in
the `data/` directory with a filename that includes a Unix timestamp for cache
busting (e.g., `martinez_pp_cases_1700000000.csv`).

The three PDFs of interest are located in the `literature/` directory:
1. Martinez - human to human Andes virus - NEJM 2020.pdf
2. Padula - human to human Andes virus - Virology 1998.pdf
3. Vial - incubation period of Andes virus - EID 2006.pdf

Running this script will produce CSV files for each table discovered. The
script is defensive – if no tables are found on a page it simply continues.
"""

import os
import time
import pdfplumber
import pandas as pd

# Directory paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LIT_DIR = os.path.join(BASE_DIR, "literature")
DATA_DIR = os.path.join(BASE_DIR, "data")

PDFS = {
    "martinez": "Martinez - human to human Andes virus - NEJM 2020.pdf",
    "padula": "Padula - human to human Andes virus - Virology 1998.pdf",
    "vial": "Vial - incubation period of Andes virus - EID 2006.pdf",
}

def timestamp() -> str:
    """Return current Unix timestamp as string for filename cache busting."""
    return str(int(time.time()))

def save_table(df: pd.DataFrame, prefix: str, page_num: int, tbl_index: int):
    """Save a DataFrame to CSV with a timestamped, descriptive filename.

    Args:
        df: DataFrame containing the extracted table.
        prefix: Short identifier for the source PDF (e.g., 'martinez').
        page_num: 1‑based page number where the table was found.
        tbl_index: Index of the table on that page (starting at 1).
    """
    ts = timestamp()
    filename = f"{prefix}_page{page_num}_tbl{tbl_index}_{ts}.csv"
    out_path = os.path.join(DATA_DIR, filename)
    df.to_csv(out_path, index=False)
    print(f"Saved table to {out_path}")

def extract_tables_from_pdf(pdf_path: str, prefix: str):
    """Extract all tables from a PDF and write them to timestamped CSV files.

    The function iterates through each page, calls ``page.extract_tables()`` and
    converts each raw table (a list‑of‑lists) into a pandas DataFrame. If the
    first row appears to be a header we use it; otherwise a generic header is
    generated.
    """
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            raw_tables = page.extract_tables()
            if not raw_tables:
                continue
            for tbl_idx, raw in enumerate(raw_tables, start=1):
                # Basic sanity check – ensure at least one row and column
                if not raw or not raw[0]:
                    continue
                # Assume first row is header if it contains any non‑numeric text
                header = raw[0]
                if any(not cell.replace(".", "", 1).isdigit() for cell in header):
                    df = pd.DataFrame(raw[1:], columns=header)
                else:
                    # Generate generic column names
                    col_count = len(header)
                    cols = [f"col_{j+1}" for j in range(col_count)]
                    df = pd.DataFrame(raw, columns=cols)
                save_table(df, prefix, i, tbl_idx)

def main():
    for key, fname in PDFS.items():
        pdf_path = os.path.join(LIT_DIR, fname)
        if not os.path.exists(pdf_path):
            print(f"⚠️ PDF not found: {pdf_path}")
            continue
        print(f"🔍 Extracting tables from {fname}")
        extract_tables_from_pdf(pdf_path, key)

if __name__ == "__main__":
    main()
