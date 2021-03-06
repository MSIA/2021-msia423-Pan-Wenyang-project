import argparse
import logging.config

from src.s3 import download_file_from_s3, upload_file_to_s3

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('s3-pipeline')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--download', default=False, action='store_true',
                        help="If True, will download the data from S3. If False, will upload data to S3")
    parser.add_argument('--s3_path', default='s3://2021-msia423-wenyang-pan/raw/pokemon.csv',
                        help="s3 data path to download or upload data")
    parser.add_argument('--local_path', default='data/sample/pokemon.csv',
                        help="local data path to store or upload data")
    args = parser.parse_args()

    if args.download:
        download_file_from_s3(args.local_path, args.s3_path)
    else:
        upload_file_to_s3(args.local_path, args.s3_path)
