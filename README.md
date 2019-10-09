# gcs-file-ingestor

Library for ingesting files into Google Cloud Storage.

The drive and use case to create this library, was when you need to create a lot of files to test some capabilities and integrations that rely on GCS. If you just need to sync files it's better to use gsutil.

The name of the folder used for ingestion, will be converted into the bucket_name.
It will traverse all children directories. You can either ingest the whole folder or ingest
a random number of files using the folder as the source. If you pass the random number of files,
the ingestor will randomly pick files and each iteration will have __{index} at the end of the file
ingested.

The files at the sample folder are taken from BigQuery public datasets.


## 1. Environment setup

### 1.1. Get the code

````bash
git clone https://.../gcs-file-ingestor.git
cd gcs-file-ingestor
````

### 1.2. Auth credentials

##### 1.2.1. Create a service account and grant it below roles

- Google Cloud Storage Editor

##### 1.2.2. Download a JSON key and save it as
- `<YOUR-CREDENTIALS_FILES_FOLDER>/gcs-file-ingestor-credentials.json`

> Please notice this folder and file will be required in next steps.

### 1.3. Virtualenv

Using *virtualenv* is optional, but strongly recommended unless you use Docker or a PEX file.

##### 1.3.1. Install Python 3.6+

##### 1.3.2. Create and activate a *virtualenv*

```bash
pip install --upgrade virtualenv
python3 -m virtualenv --python python3 env
source ./env/bin/activate
```

##### 1.3.3. Install the dependencies

```bash
pip install --editable .
```

##### 1.3.4. Set environment variables

Replace below values according to your environment:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=credentials_file_path

export PROJECT_ID=google_cloud_project_id
export SOURCE_FILE_LOCATION=./local_bucket_sync
export GCS_FILES_NUMBER=1000

```

### 1.4. Docker

See instructions below.

## 2. Sample application entry point

### 2.1. Run main.py

#### 2.1.1 Ingest all files inside folder (Recursively)

- Virtualenv

```bash
python main.py --project-id $PROJECT_ID --src-dir=$SOURCE_FILE_LOCATION create-files-from-dir
```

#### 2.1.2 Ingest random amount of files using files inside source folder

- Virtualenv

```bash
python main.py --project-id $PROJECT_ID --src-dir=$SOURCE_FILE_LOCATION create-random-number-of-files-from-dir --number-files $GCS_FILES_NUMBER
```

#### 2.1.3 Clean up files created by gcs-file-ingestor

- Virtualenv

```bash
python main.py --project-id $PROJECT_ID clean-up-buckets
```


### 2.2. Or using Docker

```bash
docker build -t gcs-file-creator .
docker run --rm --tty \
 -v CREDENTIALS_FILES_FOLDER:/data \
 -v YOUR-INGESTION_DIR:/ingestion-dir \
 gcs-file-creator \
 --project-id $PROJECT_ID \
 --src-dir=/ingestion-dir \
 create-files-from-dir
```
