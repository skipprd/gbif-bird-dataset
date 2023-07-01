import csv
import json
import argparse
from datetime import datetime
import zipfile
import io

def csv_to_json(csvFilePath):
    # open the zip file
    with zipfile.ZipFile(csvFilePath, 'r') as zf:
        # open the first file in the zip file
        with zf.open(zf.namelist()[0], 'r') as csvf:
            csvReader = csv.DictReader(io.TextIOWrapper(csvf))

            # convert each csv row into python dict and print to stdout
            for row in csvReader:
                # create a date field
                row['date'] = datetime(int(row['year']), int(row['month']), int(row['day'])).isoformat()
                print(json.dumps(row))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('csvfile', help='The ZIP file containing the CSV file to process')
    args = parser.parse_args()
    csv_to_json(args.csvfile)

if __name__ == "__main__":
    main()
