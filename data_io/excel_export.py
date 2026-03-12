# data_io/excel_export.py

import pandas as pd
from io import BytesIO


def _select_excel_engine():
    """
    Select the best available Excel engine.

    Priority:
    1. xlsxwriter (preferred for formatting)
    2. openpyxl (fallback available in most environments)

    This prevents runtime crashes if xlsxwriter is not installed.
    """

    try:
        import xlsxwriter  # noqa: F401
        return "xlsxwriter"
    except ImportError:
        pass

    try:
        import openpyxl  # noqa: F401
        return "openpyxl"
    except ImportError:
        raise ImportError(
            "No Excel writer engine available. Install one of the following:\n"
            "pip install xlsxwriter\n"
            "or\n"
            "pip install openpyxl"
        )


def create_professional_excel(df, logo_path=None):
    """
    Create a professional Excel workbook for technicians.

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

        workbook = writer.book
        worksheet = writer.sheets["Sequence"]

        # Adjust column widths
        for i, col in enumerate(df.columns):
            max_len = max(
                df[col].astype(str).map(len).max(),
                len(col)
            ) + 2
            worksheet.set_column(i, i, max_len)

        # Insert logo if supported and provided
        if logo_path and engine == "xlsxwriter":
            try:
                worksheet.insert_image("A1", logo_path, {"x_scale": 0.5, "y_scale": 0.5})
            except Exception:
                # Do not break export if logo fails
                pass

    output.seek(0)

    return output
