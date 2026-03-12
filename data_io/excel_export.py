import pandas as pd
import numpy as np
import io
import os


def create_professional_excel(df,logo_path):

    df = df.replace({np.nan:""})

    output = io.BytesIO()

    with pd.ExcelWriter(output,engine="xlsxwriter") as writer:

        df.to_excel(writer,sheet_name="TEST_SEQUENCE",index=False)

        wb = writer.book
        ws = writer.sheets["TEST_SEQUENCE"]

        header = wb.add_format({

            "bold":True,
            "align":"center",
            "border":1,
            "fg_color":"#366092",
            "font_color":"white"

        })

        for c,col in enumerate(df.columns):

            ws.write(0,c,col,header)

        ws.set_column(0,len(df.columns)-1,18)

        if os.path.exists(logo_path):

            ws.insert_image("A1",logo_path,
                {"x_scale":0.4,"y_scale":0.4}
            )

    output.seek(0)

    return output
