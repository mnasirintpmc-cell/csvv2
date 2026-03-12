# data_io/excel_export.py

import pandas as pd
import numpy as np
import io
import os
import importlib.util


# =====================================================
# ENGINE DETECTION
# =====================================================

def _get_excel_engine():
    """
    Detect available Excel engine.

    Priority:
    1. xlsxwriter
    2. openpyxl
    3. None -> let pandas auto-select
    """

    if importlib.util.find_spec("xlsxwriter") is not None:
        return "xlsxwriter"

    if importlib.util.find_spec("openpyxl") is not None:
        return "openpyxl"

    # Allow pandas to auto-detect engine instead of crashing
    return None


# =====================================================
# PROFESSIONAL EXCEL EXPORT
# =====================================================

def create_professional_excel(df, logo_path=None):

    df = df.replace({np.nan: ""})

    output = io.BytesIO()

    engine = _get_excel_engine()

    # If engine is None, pandas will attempt auto-selection
    writer_kwargs = {"engine": engine} if engine else {}

    with pd.ExcelWriter(output, **writer_kwargs) as writer:

        df.to_excel(writer, sheet_name="TEST_SEQUENCE", index=False)

        ws = writer.sheets["TEST_SEQUENCE"]

        # -------------------------------------------------
        # Formatting only supported when using xlsxwriter
        # -------------------------------------------------
        if engine == "xlsxwriter":

            wb = writer.book

            header = wb.add_format({
                "bold": True,
                "align": "center",
                "border": 1,
                "fg_color": "#366092",
                "font_color": "white"
            })

            cell = wb.add_format({
                "border": 1,
                "align": "center"
            })

            notes = wb.add_format({
                "border": 1,
                "align": "left"
            })

            # Write headers
            for c, col in enumerate(df.columns):
                ws.write(0, c, col, header)

            # Write cells
            for r in range(1, len(df) + 1):
                for c, col in enumerate(df.columns):

                    val = df.iloc[r - 1, c]

                    if pd.isna(val):
                        val = ""

                    if col == "Notes":
                        ws.write(r, c, str(val), notes)
                    else:
                        ws.write(r, c, val, cell)

            ws.set_column(0, len(df.columns) - 1, 18)

            # Instructions sheet
            instr = wb.add_worksheet("INSTRUCTIONS")

            if logo_path and os.path.exists(logo_path):

                instr.set_row(0, 120)

                try:
                    instr.insert_image(
                        "A1",
                        logo_path,
                        {"x_scale": 0.6, "y_scale": 0.6}
                    )
                except Exception:
                    pass

            instr.write(12, 1, "SEAL TEST SEQUENCE")
            instr.write(14, 1, "1. Edit sequence as required")
            instr.write(15, 1, "2. Maintain safe pressure relationships")
            instr.write(16, 1, "3. Upload file back to system")

        # -------------------------------------------------
        # Fallback formatting for other engines
        # -------------------------------------------------
        else:
            try:
                ws.column_dimensions["A"].width = 18
            except Exception:
                pass

    output.seek(0)

    return output
