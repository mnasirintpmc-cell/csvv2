# core/schema.py

TECHNICIAN_COLUMNS = [
    "Step",
    "Speed_RPM",
    "Primary seal Gas Pressure (barg)",
    "Interspace_Pressure_bar",
    "BackPressure_Drive_End_bar",
    "BackPressure_Non_Drive_End_bar",
    "Gas_Injection_bar",
    "Duration_s",
    "Acceptance point",
    "Temperature_C",
    "Gas_Type",
    "Test_Mode",
    "Measurement",
    "Torque_Check",
    "Notes"
]

MACHINE_COLUMNS_MAIN = [
    "TST_SpeedDem",
    "TST_CellPresDemand",
    "TST_InterPresDemand",
    "TST_InterBPDemand_DE",
    "TST_InterBPDemand_NDE",
    "TST_GasInjectionDemand",
    "TST_StepDuration",
    "TST_APFlag",
    "TST_TempDemand",
    "TST_GasType",
    "TST_TestMode",
    "TST_MeasurementReq",
    "TST_TorqueCheck"
]

MACHINE_COLUMNS_SEPARATION = [
    "TST_SpeedDem",
    "TST_SepSealFlwSet1",
    "TST_SepSealFlwSet2",
    "TST_SepSealPSet1",
    "TST_SepSealPSet2",
    "TST_SepSealControlTyp",
    "TST_StepDuration",
    "TST_APFlag",
    "TST_TempDemand",
    "TST_GasType",
    "TST_MeasurementReq",
    "TST_TorqueCheck"
]

# Machine → Technician column rename map (main seal)
MACHINE_TO_TECHNICIAN_MAP = {
    "TST_SpeedDem":           "Speed_RPM",
    "TST_CellPresDemand":     "Primary seal Gas Pressure (barg)",
    "TST_InterPresDemand":    "Interspace_Pressure_bar",
    "TST_InterBPDemand_DE":   "BackPressure_Drive_End_bar",
    "TST_InterBPDemand_NDE":  "BackPressure_Non_Drive_End_bar",
    "TST_GasInjectionDemand": "Gas_Injection_bar",
    "TST_StepDuration":       "Duration_s",
    "TST_APFlag":             "Acceptance point",
    "TST_TempDemand":         "Temperature_C",
    "TST_GasType":            "Gas_Type",
    "TST_TestMode":           "Test_Mode",
    "TST_MeasurementReq":     "Measurement",
    "TST_TorqueCheck":        "Torque_Check",
}

# Technician → Machine (reverse of above)
TECHNICIAN_TO_MACHINE_MAP = {v: k for k, v in MACHINE_TO_TECHNICIAN_MAP.items()}

TECHNICIAN_COLUMN_TYPES = {
    "Step":                             int,
    "Speed_RPM":                        float,
    "Primary seal Gas Pressure (barg)": float,
    "Interspace_Pressure_bar":          float,
    "BackPressure_Drive_End_bar":       float,
    "BackPressure_Non_Drive_End_bar":   float,
    "Gas_Injection_bar":                float,
    "Duration_s":                       int,
    "Acceptance point":                 int,
    "Temperature_C":                    float,
    "Gas_Type":                         str,
    "Test_Mode":                        int,
    "Measurement":                      int,
    "Torque_Check":                     int,
    "Notes":                            str,
}
