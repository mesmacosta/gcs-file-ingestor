import logging

from google.cloud import storage


class StorageClientHelper:
    __DEFAULT_LOCATION = 'us-central1'
    __DEFAULT_STORAGE_CLASS = 'COLDLINE'

    def __init__(self, project_id):
        self.__storage_cloud_client = storage.Client(project=project_id)

    def delete_bucket(self, name):
        logging.info('--> Deleting Storage Bucket...')
        bucket = self.__storage_cloud_client.get_bucket(name)
        deleted_bucket = bucket.delete(force=True)
        logging.info('Bucket deleted...')
        return deleted_bucket

    def create_bucket_with_bool_label(self,
                                      name,
                                      label,
                                      location=__DEFAULT_LOCATION,
                                      storage_class=__DEFAULT_STORAGE_CLASS):
        logging.info('--> Creating Storage Bucket...')
        bucket = storage.Bucket(name)
        bucket.location = location
        bucket.storage_class = storage_class
        bucket.name = name
        try:
            bucket = self.__storage_cloud_client.create_bucket(bucket)
            logging.info('Bucket created...')
            self.add_bool_label(bucket.name, label)
            return bucket
        except:
            logging.info('Bucket already exists...')

    def add_bool_label(self, bucket_name, label_name):
        bucket = self.__storage_cloud_client.get_bucket(bucket_name)
        labels = bucket.labels
        labels[label_name] = True
        bucket.labels = labels
        bucket.patch()

        logging.info('Updated labels on {}.'.format(bucket.name))

    def list_buckets(self):
        logging.info('--> Listing Project Storage Bucket...')

        results_iterator = self.__storage_cloud_client.list_buckets()

        results = []
        for page in results_iterator.pages:
            results.extend(page)

        return results

    def upload_file(self, bucket_name, source_file_location, destination_file_name):
        bucket = self.__storage_cloud_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_file_name)

        blob.upload_from_filename(source_file_location)
        logging.info('File created...')
