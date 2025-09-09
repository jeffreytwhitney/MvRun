import os

import pytest

from lib import Utilities


@pytest.fixture()
def reset_run_files():
    if os.path.exists("C:\\MvRun\\eof.bat"):
        os.remove("C:\\MvRun\\eof.bat")
    if os.path.exists("C:\\MvRun\\nada.iwp"):
        os.remove("C:\\MvRun\\nada.iwp")
    if os.path.exists("C:\\Microvu Programs\\eof.bat"):
        os.remove("C:\\Microvu Programs\\nada.iwp")


def test_check_local_run_files(reset_run_files):
    Utilities.check_for_local_run_files()
    assert os.path.exists("C:\\MvRun\\eof.bat")
    assert os.path.exists("C:\\MvRun\\nada.iwp")
    assert os.path.exists("C:\\Microvu Programs\\nada.iwp")
