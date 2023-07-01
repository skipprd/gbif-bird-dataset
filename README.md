# gbif-bird-dataset
Converting eBird dataset to partitioned Parquet for Pedram Navid, not that he asked.

## Usage

### Downloading the source data

Download the data from [here](https://www.gbif.org/dataset/4fa7b334-ce0d-4e88-aaae-2e0c138d049e#temporalCoverages).

### Converting the data

The data is in a large Zip in CSV format. We'll extract the zip on the fly and convert to json records and pipe to Skippr via a little python script courtesy of ChatGPT.

Skippr will discover the schema, partition the data according to our config and convert to Parquet on our local machine.

See [Skippr Docs](https://docs.skippr.io) for more info. You'll find documentation on how to sync these files to AWS S3 and Athena, and the schemas propagated to Glue Data Catalog. 

Run the following command to convert the data to partitioned Parquet files:

NOTES: 
- I've extracted the zip file to `~/Downloads/2021-eBird-dwca-1.0/eod_2021.csv` on my machine.
- You'll need to replace `INSERT_API_TOKEN_HERE` with your Skippr Metadata API token.

```bash 
python3 parse_to_json.py ~/Downloads/2021-eBird-dwca-1.0.zip | docker run -i \
-e AWS_PROFILE=skippr-test \
-e DATA_SOURCE_PLUGIN_NAME=stdin \
-e DATA_SOURCE_BATCH_SIZE_BYTES=5000000 \
-e DATA_SOURCE_BATCH_SIZE_SECONDS=30 \
-e TRANSFORM_BATCH_PARTITION_FIELDS=country \
-e TRANSFORM_BATCH_TIME_FIELDS=date \
-e TRANSFORM_BATCH_TIME_UNIT=year \
-e PIPELINE_NAME=ebirds \
-e WORKSPACE_NAME=dev \
-e SKIPPR_API_TOKEN=INSERT_API_TOKEN_HERE \
-e DATA_DIR=./data \
-v `pwd`/data:/data \
skippr/skipprd:stable
```

### Configuration Notes

`head -n 2` on the CSV file reveals the below columns. 

It's apparent that the data is partitioned contains year, month and day. So we'll use those values to create an additional field called `date` and configure `TRANSFORM_BATCH_TIME_FIELDS=date` and `TRANSFORM_BATCH_TIME_UNIT=year` to partition the data by year.

I also imagine it will be useful to partition the data by country, so we'll use `TRANSFORM_BATCH_PARTITION_FIELDS=country` to do that. 

```csv
basisofrecord
institutioncode
collectioncode
catalognumber
occurrenceid
recordedby
year
month
day
publishingcountry
country
stateprovince
county
decimallatitude
decimallongitude
locality
kingdom
phylum
class
order
family
genus
specificepithet
scientificname
vernacularname
taxonremarks
taxonconceptid
individualcount
```