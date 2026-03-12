import streamlit as st


def editable_dataframe(df):

    edited = st.data_editor(
        df,
        use_container_width=True,
        num_rows="fixed"
    )

    return edited
