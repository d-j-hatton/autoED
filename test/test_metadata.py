import pytest                             # noqa: F401
from autoed.metadata import (
    get_angle_increment_old, get_angle_increment_new, Metadata
)
from autoed.dataset import SinglaDataset
import os


@pytest.fixture(scope='session')
def datasets():

    path = os.getcwd()
    data_path_old = os.path.join(path, 'data/ED/sweep_old_text/')
    dataset_01 = SinglaDataset(data_path_old, 'sample_01')

    data_path_new = os.path.join(path, 'data/ED/sweep_new_text/')
    dataset_02 = SinglaDataset(data_path_new, 'sample_02')

    data_path_json = os.path.join(path, 'data/ED/sweep_json/')
    dataset_03 = SinglaDataset(data_path_json, 'sample_03')

    return dataset_01, dataset_02, dataset_03


def test_angle_increment_old(datasets):

    value = get_angle_increment_old(datasets[0])

    assert 0.095 < value and value < 0.11


def test_angle_increment_new(datasets):
    value = get_angle_increment_new(datasets[1])
    assert abs(value - 0.5) < 1.e-10


def test_metadata_old(datasets):

    metadata = Metadata()
    metadata.from_txt(datasets[0])

    assert abs(metadata.wavelength - 0.0250793405) < 1.e-5
    assert abs(metadata.angle_increment - 0.1) < 0.1
    assert abs(metadata.start_angle + 60.0) < 0.1
    assert abs(metadata.detector_distance - 700.00) < 0.1


def test_metadata_new(datasets):
    metadata = Metadata()
    metadata.from_txt(datasets[1])

    assert abs(metadata.wavelength - 0.03701436625) < 1.e-5
    assert abs(metadata.angle_increment - 0.5) < 0.01
    assert abs(metadata.start_angle + 20.0) < 0.1
    assert abs(metadata.detector_distance - 600.00) < 0.1


def test_metadata_json(datasets):

    metadata = Metadata()
    metadata.from_json(datasets[2])

    assert abs(metadata.wavelength - 0.026) < 1.e-4
    assert abs(metadata.angle_increment - 0.15) < 0.001
    assert abs(metadata.start_angle + 17.0) < 0.1
    assert abs(metadata.detector_distance - 333.00) < 0.1