# data_io/csv_reader.py
import pandas as pd


def load_csv(file):
    encodings = ["utf-8", "latin-1", "cp1252"]
    last_error = None
    for enc in encodings:
        try:
            if hasattr(file, "seek"):
                file.seek(0)
            return pd.read_csv(file, delimiter=";", encoding=enc)
        except Exception as e:
            last_error = e
            continue
    raise Exception(
        f"Unable to read CSV file with supported encodings. Last error: {last_error}"
    )


def safe_read_csv(file):
    return load_csv(file)
