# core/mappings.py
import pandas as pd
from core.schema import (
    MACHINE_TO_TECHNICIAN_MAP,
    TECHNICIAN_TO_MACHINE_MAP,
    TECHNICIAN_COLUMNS,
)


def convert_machine_to_technician(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename machine CSV columns to technician-friendly names,
    add missing columns with defaults, and enforce column order.
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=TECHNICIAN_COLUMNS)

    tech_df = df.rename(columns=MACHINE_TO_TECHNICIAN_MAP)

    # Add Step column if missing (use row index + 1)
    if "Step" not in tech_df.columns:
        tech_df.insert(0, "Step", range(1, len(tech_df) + 1))

    # Add Notes column if missing
    if "Notes" not in tech_df.columns:
        tech_df["Notes"] = ""

    # Keep only known technician columns that are present
    present = [c for c in TECHNICIAN_COLUMNS if c in tech_df.columns]
    tech_df = tech_df[present]

    tech_df = tech_df.sort_values("Step").reset_index(drop=True)
    return tech_df


def convert_technician_to_machine(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename technician columns back to machine CSV format,
    dropping technician-only columns (Step, Notes).
    """
    if df is None or df.empty:
        return pd.DataFrame()

    machine_df = df.copy()

    if "Step" in machine_df.columns:
        machine_df = machine_df.sort_values("Step").reset_index(drop=True)

    # Drop technician-only columns before renaming
    machine_df = machine_df.drop(columns=["Step", "Notes"], errors="ignore")

    machine_df = machine_df.rename(columns=TECHNICIAN_TO_MACHINE_MAP)

    return machine_df
