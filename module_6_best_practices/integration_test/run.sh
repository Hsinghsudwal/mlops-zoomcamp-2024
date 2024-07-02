#!/usr/bin/env bash

docker-compose up -d

sleep 5

# S3 bucket creation
aws s3 mb s3://nyc-duration --endpoint-url=http://localhost:4566

# Batch environment variables setting
export INPUT_FILE_PATTERN="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"
export S3_ENDPOINT="http://localhost:4566"

pipenv run python integration_test/test.py

# Check input file
aws s3 ls s3://nyc-duration/in/ --endpoint-url=http://localhost:4566

# Check output file
aws s3 ls s3://nyc-duration/out/ --endpoint-url=http://localhost:4566

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

docker-compose down