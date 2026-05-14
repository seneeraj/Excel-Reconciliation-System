import pandas as pd

def load_excel_file(file, sheet_name):
    df = pd.read_excel(
        file,
        sheet_name=sheet_name
    )

    df.columns = df.columns.str.strip()

    return df