# core/safety.py

import pandas as pd


def validate_safety(df: pd.DataFrame):
    """
    Validate technician sequence for potential safety issues.

    Returns a list of warning messages that the UI can display.
    The function does not modify the dataframe.
    """

    warnings = []

    if df is None or df.empty:
        warnings.append("Sequence is empty.")
        return warnings

    # Step order validation
    if "Step" in df.columns:
        if not df["Step"].is_monotonic_increasing:
            warnings.append("Step numbers are not in ascending order.")

    # Pressure validation
    if "Primary seal Gas Pressure (barg)" in df.columns:
        if (df["Primary seal Gas Pressure (barg)"] < 0).any():
            warnings.append("Negative primary seal pressure detected.")

    # Duration validation
    if "Duration_s" in df.columns:
        if (df["Duration_s"] < 0).any():
            warnings.append("Negative duration detected.")

    # Speed validation
    if "Speed_RPM" in df.columns:
        if (df["Speed_RPM"] < 0).any():
            warnings.append("Negative speed value detected.")

    return warnings
