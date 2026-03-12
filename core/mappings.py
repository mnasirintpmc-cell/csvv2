# core/mappings.py

import pandas as pd


def convert_machine_to_technician(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert machine sequence CSV format into technician-friendly format.

    This function preserves all original data but prepares the dataframe
    for technician editing and Excel export.
    """

    if df is None or df.empty:
        return pd.DataFrame()

    tech_df = df.copy()

    # Ensure Step column is sorted
    if "Step" in tech_df.columns:
        tech_df = tech_df.sort_values("Step").reset_index(drop=True)

    return tech_df


def convert_technician_to_machine(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert technician-edited dataframe back into machine CSV format.
    """

    if df is None or df.empty:
        return pd.DataFrame()

    machine_df = df.copy()

    # Ensure step order
    if "Step" in machine_df.columns:
        machine_df = machine_df.sort_values("Step").reset_index(drop=True)

    return machine_df
