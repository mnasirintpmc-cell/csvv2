
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
