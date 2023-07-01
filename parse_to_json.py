import csv
import json
import argparse
from datetime import datetime

def csv_to_json(csvFilePath):
    # read csv file
    with open(csvFilePath, 'r') as csvf:
        csvReader = csv.DictReader(csvf)

        # convert each csv row into python dict and print to stdout
        for row in csvReader:
            # create a date field
            row['date'] = datetime(int(row['year']), int(row['month']), int(row['day'])).isoformat()
            print(json.dumps(row))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('csvfile', help='The CSV file to process')
    args = parser.parse_args()
    csv_to_json(args.csvfile)

if __name__ == "__main__":
    main()
