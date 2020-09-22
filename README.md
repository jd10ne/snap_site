# Snap Site(WIP)

ScreenShot API

## Usage

```
$ curl -H "Aniapp: test" "localhost:5001?url=https://www.google.com/&url=https://www.yahoo.co.jp/"
{"https://www.google.com/":"<ScreenShot Image URL (GCS or S3 Signed URL)>","https://www.yahoo.co.jp/":"<ScreenShot Image URL (GCS or S3 Signed URL)>"}
```

## Requirements
- Python 3
- Pipenv or Pip
- Docker
- AWS S3 Bucket or Google Cloud Storage Bucket
- AWS ECR or Google Container Registory

- Option (IAM Credential for manipulating storage)
    - You need these credential to launch this application on local docker.
        - AWS IAM User access key
        - GCP Service Account Key


## Docker Build

```
docker build -t snap-api .
```

## Local Launch

```
docker run -itp 5001:5001 --env-file ./env.list  \
    -v $GOOGLE_APPLICATION_CREDENTIALS:/tmp/keys/<GCP SERVICE ACCOUNT CREDENTIAL JSON>:ro \
    snap-api
```

## Deploy

- Google Cloud Run + Cloud Storage
    - Settings (Required)
        - Environment Variable
            - BUCKET=<GCS bucket naem>
            - ACCEPT_STR=test
            - ACCEPT_HEADER=Aniapp
            - PROVIDER=GCP
```
# Image push to Container Registory
docker build . --tag gcr.io/snap-api-290208/snap-api
docker push gcr.io/snap-api-290208/snap-api

# Please setup Cloud Run on the console
```