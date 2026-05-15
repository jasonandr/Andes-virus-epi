import pandas as pd
import glob
import os

def main():
    files = glob.glob('/Users/jasonandrews/repos/hanta/literature/*.xlsx')
    for f in sorted(files):
        print(f"\n{'='*50}")
        print(f"File: {os.path.basename(f)}")
        try:
            # Read all sheets
            xls = pd.ExcelFile(f)
            for sheet in xls.sheet_names:
                print(f"\nSheet: {sheet}")
                df = pd.read_excel(f, sheet_name=sheet)
                print(f"Columns: {df.columns.tolist()}")
                print(df.head(3))
        except Exception as e:
            print(f"Error reading file: {e}")

if __name__ == "__main__":
    main()
