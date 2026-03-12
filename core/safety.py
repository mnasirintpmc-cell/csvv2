# core/safety.py

def validate_pressure(df):

    warnings = []

    if "Primary seal Gas Pressure (barg)" not in df.columns:
        return warnings

    for i,row in df.iterrows():

        primary = float(row["Primary seal Gas Pressure (barg)"])
        inter = float(row["Interspace_Pressure_bar"])

        if inter > primary:

            warnings.append(
                f"Step {row['Step']}: Interspace pressure greater than primary"
            )

        if primary - inter < 0.2 and inter > 0:

            warnings.append(
                f"Step {row['Step']}: ΔP below 0.2 bar"
            )

    return warnings
