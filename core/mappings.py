# core/mappings.py

def machine_to_technician(df, mapping):

    tech = df.rename(columns=mapping)

    tech.insert(0, "Step", range(1, len(tech)+1))

    if "Notes" not in tech.columns:
        tech["Notes"] = ""

    return tech


def technician_to_machine(df, reverse_mapping):

    machine = df.rename(columns=reverse_mapping)

    machine = machine.drop(columns=["Step","Notes"], errors="ignore")

    return machine
