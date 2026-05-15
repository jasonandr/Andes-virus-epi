import pdfplumber
import pandas as pd
import numpy as np

def main():
    pdf_path = "/Users/jasonandrews/repos/hanta/literature/nejmoa2009040_appendix_1.pdf"
    
    with pdfplumber.open(pdf_path) as pdf:
        # Based on previous output, Table S2 is on page 25 (index 24)
        page = pdf.pages[24]
        
        # Extract tables
        tables = page.extract_tables()
        if not tables:
            print("No tables found by default extractor. Falling back to text parsing.")
            return
            
        # The first table should be Table S2
        table = tables[0]
        
        # Convert to DataFrame
        # The headers might be split across multiple rows, let's just use raw data and clean it
        df = pd.DataFrame(table[1:], columns=table[0])
        
        # We will save the raw table first
        csv_path = "/Users/jasonandrews/repos/hanta/data/epuyen_2018_actual_cases_raw.csv"
        df.to_csv(csv_path, index=False)
        print(f"Extracted actual Epuyén line list to {csv_path}")
        print(df.head())

if __name__ == "__main__":
    main()
