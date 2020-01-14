Altering a CSV file and writing the temp file back.

```
#!/usr/bin/python3

import os
import sys
import argparse
import shutil
import csv
import collections
from tempfile import NamedTemporaryFile

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=str, help="CSV file.")
    args = parser.parse_args()

    if len(sys.argv) < 3:
        sys.exit("Error: not enough args")

    filename = args.csv
    tempfile = NamedTemporaryFile(mode='w', delete=False)

    fields = ['file', 'key', 'EN_value', 'ES_value']

    with open(filename, 'r', encoding='utf8') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            row['file'] = 'blah.txt'
            # add logic to replace fila name here
            row = {'file': row['file'], 'key': row['key'], 'EN_value': row['EN_value'], 'ES_value': row['ES_value']}
            writer.writerow(row)

    shutil.move(tempfile.name, 'new_' + filename)


if __name__ == "__main__":
    main()
```
