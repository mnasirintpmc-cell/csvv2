# core/safety.py
import pandas as pd


def validate_safety(df: pd.DataFrame) -> dict:
    """
    Validate technician sequence for safety issues.

    Returns:
        dict with keys:
            "errors"   - blockers that must be fixed before proceeding
            "warnings" - advisories the technician should review
    """
    errors = []
    warnings = []

    if df is None or df.empty:
        errors.append("Sequence is empty.")
        return {"errors": errors, "warnings": warnings}

    # Step order
    if "Step" in df.columns:
        if not df["Step"].is_monotonic_increasing:
            warnings.append("Step numbers are not in ascending order.")

    # Primary pressure — negative
    pres_col = "Primary seal Gas Pressure (barg)"
    if pres_col in df.columns:
        if df[pres_col].isna().any():
            bad = df.loc[df[pres_col].isna(), "Step"].tolist()
            errors.append(f"Missing primary pressure on steps: {bad}")
        if (df[pres_col].fillna(0) < 0).any():
            errors.append("Negative primary seal pressure detected.")

    # Primary must exceed back pressure
    if pres_col in df.columns and "BackPressure_Drive_End_bar" in df.columns:
        mask = df[pres_col].fillna(0) <= df["BackPressure_Drive_End_bar"].fillna(0)
        if mask.any():
            bad = df.loc[mask, "Step"].tolist()
            errors.append(
                f"Primary pressure must exceed back pressure. Check steps: {bad}"
            )

    # Negative duration
    if "Duration_s" in df.columns:
        if (df["Duration_s"].fillna(0) < 0).any():
            errors.append("Negative duration detected.")

    # Negative speed
    if "Speed_RPM" in df.columns:
        if (df["Speed_RPM"].fillna(0) < 0).any():
            errors.append("Negative speed value detected.")

    # Acceptance point with zero duration
    if "Acceptance point" in df.columns and "Duration_s" in df.columns:
        mask = (df["Acceptance point"] == 1) & (df["Duration_s"].fillna(0) == 0)
        if mask.any():
            bad = df.loc[mask, "Step"].tolist()
            warnings.append(
                f"Acceptance point steps with zero duration: {bad}"
            )

    return {"errors": errors, "warnings": warnings}
