import logging
import os
import random

from .gcs_storage_client_helper import StorageClientHelper


class GCSFileIngestor:
    __FILE_INGESTOR_GCS_LABEL = 'gcs_file_ingestor'

    def __init__(self, project_id):
        self.__storage_helper = StorageClientHelper(project_id)
        self.__project_id = project_id

    def create_files_from_dir(self, dir):
        files_obj = self.__scrape_files(dir)
        for file_obj in files_obj:
            logging.info(file_obj)
            self.__storage_helper.create_bucket_with_bool_label(
                file_obj['bucket_name'], GCSFileIngestor.__FILE_INGESTOR_GCS_LABEL)
            self.__storage_helper.upload_file(
                file_obj['bucket_name'],
                file_obj['source_file_location'],
                file_obj['destination_file_name'])

    def create_random_number_of_files_from_dir(self, number, dir):
        files_obj = self.__scrape_files(dir)
        for i in range(number):
            file_obj = random.choice(files_obj)
            new_file_obj = file_obj.copy()
            destination_file_name = new_file_obj['destination_file_name']
            new_file_obj['destination_file_name'] = \
                destination_file_name.replace('.', f'__{i}.')
            logging.info(new_file_obj)
            self.__storage_helper.create_bucket_with_bool_label(
                new_file_obj['bucket_name'], GCSFileIngestor.__FILE_INGESTOR_GCS_LABEL)
            self.__storage_helper.upload_file(
                new_file_obj['bucket_name'],
                new_file_obj['source_file_location'],
                new_file_obj['destination_file_name'])

    def clean_up_buckets(self):
        buckets = self.__storage_helper.list_buckets()
        for bucket in buckets:
            gcs_file_creator = bucket.labels.get(GCSFileIngestor.__FILE_INGESTOR_GCS_LABEL)
            if gcs_file_creator == 'true':
                self.__storage_helper.delete_bucket(bucket.name)

    @classmethod
    def __scrape_files(cls, dir):
        files_obj = []
        for dir_name, subdir_list, file_list in os.walk(dir):
            for file_name in file_list:
                if file_name.endswith('.csv'):
                    bucket_name = dir.split('/')[-1].replace('./', '')
                    file_location = dir_name.split(f'{dir}/', 1)
                    # It means we are not at the root dir
                    if len(file_location) > 1:
                        file_location = file_location[1]
                        destination_file_name = f'{file_location}/{file_name}'
                    else:
                        destination_file_name = file_name

                    source_file_location = f'{dir_name}/{file_name}'
                    files_obj.append({
                        'bucket_name': bucket_name,
                        'source_file_location': source_file_location,
                        'destination_file_name': destination_file_name
                    })
        return files_obj
