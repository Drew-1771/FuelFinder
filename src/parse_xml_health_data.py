# Importing the required libraries
import xml.etree.ElementTree as Xet
import pandas as pd
from pathlib import Path

ROOT = Path.cwd()

cols, cols1 = (
    [
        "id",
        "index",
        "date",
        "step_count",
        "active_calories_burned",
        "resting_calories_burned",
    ],
    ["height", "weight", "age", "sex"],
)

rows, rows1 = [], [None, None, None, None]

# Parsing the XML file
xmlparse = Xet.parse(Path.cwd() / "data" / "apple_health_export" / "export.xml")
root = xmlparse.getroot()

stats = set()
for index, child in enumerate(root):
    try:
        stats.add(child.attrib["type"])
        record = child.attrib
        step_count, active_calories_burned, resting_calories_burned = None, None, None
        if record["type"] == "HKQuantityTypeIdentifierStepCount":
            step_count = record["value"]
        if record["type"] == "HKQuantityTypeIdentifierActiveEnergyBurned":
            active_calories_burned = record["value"]
        if record["type"] == "HKQuantityTypeIdentifierBasalEnergyBurned":
            resting_calories_burned = record["value"]
        if record["type"] == "HKQuantityTypeIdentifierHeight":
            rows1[0] = record["value"]
        if record["type"] == "HKQuantityTypeIdentifierBodyMass":
            rows1[1] = record["value"]
        if record["type"] == "HKCharacteristicTypeIdentifierBiologicalSex":
            rows1[2] = record["value"]
        if record["type"] == "HKCharacteristicTypeIdentifierDateOfBirth":
            rows1[3] = record["value"]

        rows.append(
            {
                "id": 42,  # currently running for my stats
                "index": index,
                "date": record["endDate"],
                "step_count": step_count,
                "active_calories_burned": active_calories_burned,
                "resting_calories_burned": resting_calories_burned,
            }
        )
    except KeyError:
        pass

pd.DataFrame(rows, columns=cols).to_csv(
    ROOT / "data" / f"health_stats - health_data_user{42}.csv"
)
pd.DataFrame(rows1, columns=cols1).to_csv(
    ROOT / "data" / f"health_stats - user{42}.csv"
)

# show valid metrics
print("Valid metrics:")
for metric in stats:
    print(f"\t{metric}")
