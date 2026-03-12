# data_io/excel_export.py

import pandas as pd
from io import BytesIO
import importlib.util


def _select_excel_engine():
    """
    Select the best available Excel engine.

    Priority:
    1. xlsxwriter
    2. openpyxl

    The environment must provide at least one engine through
    requirements.txt. Runtime installation is not attempted
    because cloud environments are read-only.
    """

    if importlib.util.find_spec("xlsxwriter") is not None:
        return "xlsxwriter"

    if importlib.util.find_spec("openpyxl") is not None:
        return "openpyxl"

    raise ImportError(
        "No Excel writer engine available. "
        "Add 'xlsxwriter' or 'openpyxl' to requirements.txt"
    )


def create_professional_excel(df, logo_path=None):
    """
    Create a professional Excel workbook for technician sequences.

    Parameters
    ----------
    df : pandas.DataFrame
        Technician dataframe to export.

    logo_path : str | None
        Optional path to company logo.

    Returns
    -------
    BytesIO
        Excel file buffer ready for Streamlit download.
    """

    output = BytesIO()

    engine = _select_excel_engine()

    with pd.ExcelWriter(output, engine=engine) as writer:

        df.to_excel(writer, index=False, sheet_name="Sequence")

        worksheet = writer.sheets["Sequence"]

        # Auto column sizing
        for i, col in enumerate(df.columns):

            try:
                max_len = max(
                    df[col].astype(str).map(len).max(),
                    len(col)
                ) + 2
            except Exception:
                max_len = len(col) + 2

            worksheet.set_column(i, i, max_len)

        # Insert logo if supported
        if logo_path and engine == "xlsxwriter":
            try:
                worksheet.insert_image(
                    "A1",
                    logo_path,
                    {"x_scale": 0.5, "y_scale": 0.5}
                )
            except Exception:
                pass

    output.seek(0)

    return output
