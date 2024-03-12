# Importing the required libraries
import xml.etree.ElementTree as Xet
import pandas as pd
from pathlib import Path

ROOT = Path.cwd()

cols = [
    "index",
    "date",
    "step_count",
    "active_calories_burned",
    "resting_calories_burned",
]
rows = []

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
        rows.append(
            {
                "date": record["endDate"],
                "step_count": step_count,
                "active_calories_burned": active_calories_burned,
                "resting_calories_burned": resting_calories_burned,
            }
        )
    except KeyError:
        pass

pd.DataFrame(rows, columns=cols).to_csv(ROOT / "data" / "health_stats.csv")

# show valid metrics
print("Valid metrics:")
for metric in stats:
    print(f"\t{metric}")
