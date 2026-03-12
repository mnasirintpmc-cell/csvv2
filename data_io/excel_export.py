# data_io/excel_export.py

import pandas as pd
from io import BytesIO
import importlib
import subprocess
import sys


def _ensure_excel_engine():
    """
    Ensure an Excel writer engine is available.

    Priority:
    1. xlsxwriter
    2. openpyxl

    If neither exists, automatically install xlsxwriter.
    """

    # Try xlsxwriter
    if importlib.util.find_spec("xlsxwriter") is not None:
        return "xlsxwriter"

    # Try openpyxl
    if importlib.util.find_spec("openpyxl") is not None:
        return "openpyxl"

    # Install xlsxwriter automatically
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "xlsxwriter"]
        )
    except Exception as e:
        raise ImportError(
            "Unable to install required Excel engine 'xlsxwriter'."
        ) from e

    return "xlsxwriter"


def create_professional_excel(df, logo_path=None):
    """
    Create a professional Excel workbook for technician sequences.

    Parameters
    ----------
    df : pandas.DataFrame
        Data to export.

    logo_path : str | None
        Optional company logo.

    Returns
    -------
    BytesIO
        Excel file buffer suitable for Streamlit download.
    """

    output = BytesIO()

    engine = _ensure_excel_engine()

    with pd.ExcelWriter(output, engine=engine) as writer:

        df.to_excel(writer, index=False, sheet_name="Sequence")

        workbook = writer.book
        worksheet = writer.sheets["Sequence"]

        # Adjust column width dynamically
        for i, col in enumerate(df.columns):

            try:
                max_len = max(
                    df[col].astype(str).map(len).max(),
                    len(col)
                ) + 2
            except Exception:
                max_len = len(col) + 2

            worksheet.set_column(i, i, max_len)

        # Insert logo if engine supports it
        if logo_path and engine == "xlsxwriter":
            try:
                worksheet.insert_image(
                    "A1",
                    logo_path,
                    {"x_scale": 0.5, "y_scale": 0.5}
                )
            except Exception:
                # Logo failure should not break export
                pass

    output.seek(0)

    return output
