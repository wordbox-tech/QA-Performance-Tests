import csv
from typing import Dict
from typing import Final
from typing import List


EMPTY_STRING: Final[str] = ""
WRITE_MODE: Final[str] = "w"


def export_to_csv(file_name: str, field_names: List[str], data: List[Dict]):
    with open(file=file_name, mode=WRITE_MODE, newline=EMPTY_STRING) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=field_names,
        )
        for row in data:
            writer.writerow(row)
