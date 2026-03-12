import streamlit as st
import pandas as pd
import os

from io.csv_reader import safe_read_csv
from io.excel_export import create_professional_excel
from io.spec_scanner import scan_spec

from core.mappings import convert_machine_to_technician, convert_technician_to_machine
from core.safety import validate_safety

from ui.editor import editable_dataframe


BASE_DIR = os.path.dirname(__file__)

MAIN_TEMPLATE = os.path.join(BASE_DIR,"templates/MainSealSet2.csv")
SEP_TEMPLATE = os.path.join(BASE_DIR,"templates/SeperationSeal.csv")

st.set_page_config(layout="wide")
st.title("⚙️ Seal Test Manager")

seal_type = st.sidebar.selectbox(
"Seal Type",
["Main Seal","Separation Seal"]
)

template = MAIN_TEMPLATE if seal_type=="Main Seal" else SEP_TEMPLATE

operation = st.sidebar.radio(

"Operation",

[
"Download Template",
"Machine CSV → Technician Excel",
"Technician Excel → Machine CSV",
"Spec → Technician Excel"
]

)


# --------------------------------------------------
# DOWNLOAD TEMPLATE
# --------------------------------------------------

if operation=="Download Template":

    df = safe_read_csv(template)

    tech_df = convert_machine_to_technician(df)

    excel = create_professional_excel(
        tech_df,
        os.path.join(BASE_DIR,"templates/company_logo.png")
    )

    st.download_button(
        "Download Technician Template",
        excel.getvalue(),
        "technician_template.xlsx"
    )


# --------------------------------------------------
# MACHINE CSV → TECHNICIAN
# --------------------------------------------------

elif operation=="Machine CSV → Technician Excel":

    uploaded = st.file_uploader("Upload Machine CSV",type=["csv"])

    if uploaded:

        df = safe_read_csv(uploaded)

        tech_df = convert_machine_to_technician(df)

        edited = editable_dataframe(tech_df)

        warnings = validate_safety(edited)

        for w in warnings:
            st.warning(w)

        excel = create_professional_excel(
            edited,
            os.path.join(BASE_DIR,"templates/company_logo.png")
        )

        st.download_button(
            "Download Technician Excel",
            excel.getvalue(),
            "technician_sequence.xlsx"
        )


# --------------------------------------------------
# TECHNICIAN → MACHINE CSV
# --------------------------------------------------

elif operation=="Technician Excel → Machine CSV":

    uploaded = st.file_uploader("Upload Technician Excel",type=["xlsx"])

    if uploaded:

        df = pd.read_excel(uploaded)

        edited = editable_dataframe(df)

        machine_df = convert_technician_to_machine(edited)

        csv = machine_df.to_csv(index=False,sep=";")

        st.download_button(
            "Download Machine CSV",
            csv,
            "machine_sequence.csv"
        )


# --------------------------------------------------
# SPEC → TECHNICIAN
# --------------------------------------------------

elif operation=="Spec → Technician Excel":

    uploaded = st.file_uploader("Upload Spec (.xlsb)",type=["xlsb"])

    if uploaded:

        spec_df = scan_spec(uploaded)

        edited = editable_dataframe(spec_df)

        warnings = validate_safety(edited)

        for w in warnings:
            st.warning(w)

        excel = create_professional_excel(
            edited,
            os.path.join(BASE_DIR,"templates/company_logo.png")
        )

        st.download_button(
            "Download Technician Excel",
            excel.getvalue(),
            "technician_sequence.xlsx"
        )
