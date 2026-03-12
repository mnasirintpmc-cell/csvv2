# data_io/csv_reader.py

import pandas as pd


def load_csv(file):
    """
    Internal CSV loader with encoding fallbacks.

    Attempts multiple encodings to ensure compatibility with
    machine-generated CSV files that may not use UTF-8.

    Parameters
    ----------
    file : file-like object or path
        CSV file input.

    Returns
    -------
    pandas.DataFrame
        Parsed CSV dataframe.
    """

    encodings = ["utf-8", "latin-1", "cp1252"]

    for enc in encodings:
        try:
            return pd.read_csv(file, delimiter=";", encoding=enc)
        except Exception:
            continue

    raise Exception("Unable to read CSV file with supported encodings.")


def safe_read_csv(file):
    """
    Public API used across the application.

    Wrapper around `load_csv` to provide a stable import interface
    for application modules such as seal_test_manager.py.

    This preserves backward compatibility and allows future
    enhancements such as logging, validation, or schema enforcement.
    """

    return load_csv(file)
