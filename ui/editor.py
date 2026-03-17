# ui/editor.py
import streamlit as st
import pandas as pd


def editable_dataframe(df: pd.DataFrame, key: str = "editor") -> pd.DataFrame:
    """
    Render an editable dataframe using st.data_editor.
    Returns the edited dataframe.
    """
    if df is None or df.empty:
        st.warning("No data to display.")
        return df

    edited = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key=key
    )
    return edited
