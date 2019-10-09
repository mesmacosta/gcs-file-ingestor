import argparse
import logging

from .gcs_file_ingestor import GCSFileIngestor


class GCSFileIngestorCLI:

    @classmethod
    def run(cls):
        cls.__setup_logging()
        cls.__parse_args()

    @classmethod
    def __setup_logging(cls):
        logging.basicConfig(level=logging.INFO)

    @classmethod
    def __parse_args(cls):
        parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        parser.add_argument('--project-id', help='Project id', required=True)
        parser.add_argument('--src-dir', help='Source dir with csv files')

        parser.set_defaults(func=lambda *inner_args: logging.info('Must use a subcommand'))

        subparsers = parser.add_subparsers()

        create_files_from_dir_parser = subparsers.add_parser('create-files-from-dir',
                                                             help='Create files from source dir')
        create_files_from_dir_parser.set_defaults(func=cls.__create_files_from_dir)

        create_random_number_of_files_from_dir_parser = subparsers.add_parser(
            'create-random-number-of-files-from-dir',
            help='Create the supplied number of files from source dir, files are chosen randomly')
        create_random_number_of_files_from_dir_parser.add_argument('--number-files',
                                                                   help='Number of files',
                                                                   required=True)
        create_random_number_of_files_from_dir_parser.set_defaults(
            func=cls.__create_random_number_of_files_from_dir)

        clean_up_parser = subparsers.add_parser(
            'clean-up-buckets',
            help='Clean up only the buckets created by the File Creator')
        clean_up_parser.set_defaults(func=cls.__clean_up_buckets)

        args = parser.parse_args()
        args.func(args)

    @classmethod
    def __create_files_from_dir(cls, args):
        GCSFileIngestor(args.project_id).create_files_from_dir(dir=args.src_dir)

    @classmethod
    def __create_random_number_of_files_from_dir(cls, args):
        GCSFileIngestor(args.project_id).create_random_number_of_files_from_dir(
            number=int(args.number_files),dir=args.src_dir)

    @classmethod
    def __clean_up_buckets(cls, args):
        GCSFileIngestor(args.project_id).clean_up_buckets()
