import random
import math
import clickhouse_connect
import os
from datetime import datetime, timezone
import time

def generate_measurements(feeder_id):
    # Nominal line-to-line voltage: 12 kV
    voltage = 12.0

    # Simulate different electrical loads
    # Baseline current for each feeder (in amps)
    feeder_loads = {
        1: 100,  # Residential
        2: 150,  # Commercial
        3: 200,  # Industrial
        4: 125   # Mixed-use
    }

    # Get this feeder's baseline current
    base_current = feeder_loads[feeder_id]

    # Add small random fluctuations
    current = base_current + random.uniform(-10, 10)

    # Add small voltage fluctuations
    voltage_a = voltage + random.uniform(-0.1, 0.1)
    voltage_b = voltage + random.uniform(-0.1, 0.1)
    voltage_c = voltage + random.uniform(-0.1, 0.1)

    # Add small current differences between phases
    current_a = current + random.uniform(-5, 5)
    current_b = current + random.uniform(-5, 5)
    current_c = current + random.uniform(-5, 5)

    # Assume an inductive load with a power factor of 0.95
    power_factor = 0.95

    # Use average phase current and voltage
    avg_voltage = (voltage_a + voltage_b + voltage_c) / 3
    avg_current = (current_a + current_b + current_c) / 3

    # Calculate three-phase real power in MW
    mw = (math.sqrt(3) * avg_voltage * avg_current * power_factor) / 1000

    # Calculate three-phase reactive power in MVAR
    mvar = (math.sqrt(3) * avg_voltage * avg_current *
            math.sqrt(1 - power_factor**2)) / 1000


    # We don't return average so that way small variations in data are not lost
    # We can do average on grafana if we so desire
    return {
        "feeder_id": feeder_id,
        "voltage_a": voltage_a,
        "voltage_b": voltage_b,
        "voltage_c": voltage_c,
        "current_a": current_a,
        "current_b": current_b,
        "current_c": current_c,
        "mw": mw,
        "mvar": mvar
    }

# Creation of the Click House DB connection
client = clickhouse_connect.get_client(
    host=os.environ["CLICKHOUSE_HOST"],
    username=os.environ["CLICKHOUSE_USER"],
    password=os.environ["CLICKHOUSE_PASSWORD"],
    database=os.environ["CLICKHOUSE_DATABASE"]
)

while True:

    for feeder_id in range(1, 5):
        measurements = generate_measurements(feeder_id)

        client.insert(
            "feeder_measurements",
            [[
                datetime.now(timezone.utc),
                feeder_id,
                measurements["voltage_a"],
                measurements["voltage_b"],
                measurements["voltage_c"],
                measurements["current_a"],
                measurements["current_b"],
                measurements["current_c"],
                measurements["mw"],
                measurements["mvar"]
            ]],
            column_names=[
                "timestamp",
                "feeder_id",
                "voltage_a",
                "voltage_b",
                "voltage_c",
                "current_a",
                "current_b",
                "current_c",
                "mw",
                "mvar"
            ]
        )

    print("Inserted measurements for all 4 feeders", flush=True)

    time.sleep(5)
