#!/usr/bin/env python3
import sys
import os
import argparse
import argcomplete
from .dataset import SinglaDataset


# PYTHON_ARGCOMPLETE_OK
def main():

    msg = 'Script for automatic processing of existing Singla data'
    parser = argparse.ArgumentParser(description=msg)
    parser.add_argument('dirname', nargs='?', default=None,
                        help='Name of the directory to watch')
    parser.add_argument('--pid', nargs='?', type=int,
                        default=None,
                        help='PID of the process to kill')

    argcomplete.autocomplete(parser)

    args = parser.parse_args()

    if args.dirname:
        process_dir(args.dirname)
    else:
        parser.print_help()
        sys.exit(1)


def process_dir(dir_name):
    """The function to search a directory recursively,
    convert all unprocessed files to nexgen and process
    them with xia2
    """

    dir_path = os.path.abspath(dir_name)

    if not os.path.exists(dir_path):
        print("Directory %s does not exist" % dir_path)
        return
    if not os.path.isdir(dir_path):
        print('%s is not a directory' % dir_path)

    # Search for any master files
    master_files = gather_master_files(dir_path)
    for master_file in master_files:
        basename = master_file[:-12]
        dataset = SinglaDataset.from_basename(basename)

        dataset.search_and_update_data_files()

        if dataset.all_files_present():

            if not os.path.exists(dataset.nexgen_file):
                dataset.set_logger()
                print('Processing ', dataset.base)
                dataset.process()


def gather_master_files(directory):
    master_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith('__master.h5'):
                master_files.append(file_path)

    return master_files


if __name__ == '__main__':
    main()