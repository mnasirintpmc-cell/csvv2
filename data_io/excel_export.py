# data_io/excel_export.py

import pandas as pd
import numpy as np
import io
import os


def create_professional_excel(df, logo_path=None):
    """
    Create formatted Excel file identical to the original working implementation.
    """

    df = df.replace({np.nan: ""})

    output = io.BytesIO()

    # Use same behaviour as original working version
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:

        df.to_excel(writer, sheet_name="TEST_SEQUENCE", index=False)

        wb = writer.book
        ws = writer.sheets["TEST_SEQUENCE"]

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

        # Write data rows
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

        # Instructions sheet (same as original)
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

    output.seek(0)

    return output
