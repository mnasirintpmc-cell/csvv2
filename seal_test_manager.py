# seal_test_manager.py
import streamlit as st
import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from data_io.csv_reader import safe_read_csv
from data_io.excel_export import create_professional_excel
from data_io.spec_scanner import scan_spec
from core.mappings import convert_machine_to_technician, convert_technician_to_machine
from core.safety import validate_safety
from ui.editor import editable_dataframe

MAIN_TEMPLATE = os.path.join(BASE_DIR, "templates/MainSealSet2.csv")
SEP_TEMPLATE  = os.path.join(BASE_DIR, "templates/SeperationSeal.csv")
LOGO_PATH     = os.path.join(BASE_DIR, "templates/company_logo.png")

st.set_page_config(layout="wide")
st.title("⚙️ Seal Test Manager")

seal_type = st.sidebar.selectbox("Seal Type", ["Main Seal", "Separation Seal"])
template  = MAIN_TEMPLATE if seal_type == "Main Seal" else SEP_TEMPLATE

operation = st.sidebar.radio(
    "Operation",
    [
        "Download Template",
        "Machine CSV → Technician Excel",
        "Technician Excel → Machine CSV",
        "Spec → Technician Excel",
    ]
)


def show_safety(result: dict):
    """Display structured safety validation results."""
    for e in result.get("errors", []):
        st.error(f"🔴 INTERLOCK: {e}")
    for w in result.get("warnings", []):
        st.warning(f"🟡 Advisory: {w}")
    if not result["errors"] and not result["warnings"]:
        st.success("✅ No safety issues found.")


# --------------------------------------------------
# DOWNLOAD TEMPLATE
# --------------------------------------------------
if operation == "Download Template":
    if not os.path.exists(template):
        st.error(f"Template file not found: {template}")
    else:
        df     = safe_read_csv(template)
        tech_df = convert_machine_to_technician(df)
        excel  = create_professional_excel(tech_df, LOGO_PATH)
        st.download_button(
            "⬇️ Download Technician Template",
            excel.getvalue(),
            "technician_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# --------------------------------------------------
# MACHINE CSV → TECHNICIAN
# --------------------------------------------------
elif operation == "Machine CSV → Technician Excel":
    uploaded = st.file_uploader("Upload Machine CSV", type=["csv"])
    if uploaded:
        df      = safe_read_csv(uploaded)
        tech_df = convert_machine_to_technician(df)
        edited  = editable_dataframe(tech_df, key="machine_to_tech")
        result  = validate_safety(edited)
        show_safety(result)
        if not result["errors"]:
            excel = create_professional_excel(edited, LOGO_PATH)
            st.download_button(
                "⬇️ Download Technician Excel",
                excel.getvalue(),
                "technician_sequence.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("Fix interlock errors before downloading.")

# --------------------------------------------------
# TECHNICIAN → MACHINE CSV
# --------------------------------------------------
elif operation == "Technician Excel → Machine CSV":
    uploaded = st.file_uploader("Upload Technician Excel", type=["xlsx"])
    if uploaded:
        df         = pd.read_excel(uploaded)
        edited     = editable_dataframe(df, key="tech_to_machine")
        result     = validate_safety(edited)
        show_safety(result)
        if not result["errors"]:
            machine_df = convert_technician_to_machine(edited)
            csv        = machine_df.to_csv(index=False, sep=";")
            st.download_button(
                "⬇️ Download Machine CSV",
                csv,
                "machine_sequence.csv",
                mime="text/csv"
            )
        else:
            st.error("Fix interlock errors before downloading.")

# --------------------------------------------------
# SPEC → TECHNICIAN
# --------------------------------------------------
elif operation == "Spec → Technician Excel":
    uploaded = st.file_uploader("Upload Spec (.xlsb)", type=["xlsb"])
    if uploaded:
        spec_df = scan_spec(uploaded)
        if spec_df.empty:
            st.error("No test steps found in spec file. Check the sheet structure.")
        else:
            edited = editable_dataframe(spec_df, key="spec_to_tech")
            result = validate_safety(edited)
            show_safety(result)
            if not result["errors"]:
                excel = create_professional_excel(edited, LOGO_PATH)
                st.download_button(
                    "⬇️ Download Technician Excel",
                    excel.getvalue(),
                    "technician_sequence.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("Fix interlock errors before downloading.")
