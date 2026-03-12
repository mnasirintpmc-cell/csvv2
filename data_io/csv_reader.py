# io/csv_reader.py

import pandas as pd

def load_csv(file):

    encodings = ["utf-8","latin-1","cp1252"]

    for enc in encodings:

        try:
            return pd.read_csv(file, delimiter=";", encoding=enc)

        except:
            continue

    raise Exception("Unable to read CSV file")
