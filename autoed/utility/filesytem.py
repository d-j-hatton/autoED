"""Keeps some useful functions that operate on the filesystem"""
import os
from autoed.dataset import SinglaDataset


def gather_master_files(directory):
    """
    Given a directory path return all the paths of all files ending with
    '_master.h5'
    """

    master_files = []

    if not os.path.exists(directory):
        return []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith('_master.h5'):
                master_files.append(file_path)

    return master_files


def gather_datasets(dir_path):
    """ Given a directory path return all the Singla datasets in that path """

    datasets = []
    master_files = gather_master_files(dir_path)
    for master_file in master_files:
        basename = master_file[:-10]
        dataset = SinglaDataset.from_basename(basename)

        dataset.search_and_update_data_files()

        datasets.append(dataset)

    return datasets
