from os import path

import pytest

from lib.Utilities import resolve_path


@pytest.fixture(scope="session")
def test_dir():  # sourcery skip: no-conditionals-in-tests
    test_dir = resolve_path()
    if not test_dir.endswith("test"):
        test_dir = path.join(test_dir, "test")
    return test_dir


@pytest.fixture(scope="session")
def input_dir(test_dir):
    return path.join(test_dir, "input")


@pytest.fixture(scope="session")
def output_dir(test_dir):
    return path.join(test_dir, "output")


@pytest.fixture(scope="session")
def salted_path(input_dir):
    return path.join(input_dir, "446007_REV G\\446007 DATUM A UP.iwp")


@pytest.fixture(scope="session")
def unsalted_path(input_dir):
    return path.join(input_dir, "446007_REV G\\446007 DATUM F UP.iwp")


@pytest.fixture(scope="session")
def mv_rotary_path(input_dir):
    return path.join(input_dir, "2030-6516-1300 REV B\\2030-6516-1300.iwp")


@pytest.fixture(scope="session")
def mv_smart_profile_path(input_dir):
    return path.join(input_dir, "446007_REV G\\446007 ITEM 1 PROFILE.iwp")


@pytest.fixture(scope="session")
def mv_multipart_path(input_dir):
    return path.join(input_dir, "110017557-B REV E\\110017557-B SIDE VIEW MULTI.iwp")
