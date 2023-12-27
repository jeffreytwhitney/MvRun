import os
import sys

this = sys.modules[__name__]

recent_files_filepath = ""


def _write_recent_files(file_lines: list[str]):
    list_filepath = _get_recentfiles_filepath()
    with open(list_filepath, "w") as f:
        for file in file_lines:
            f.write(f"{file.strip()}\n")


def _get_recentfiles_filepath() -> str:
    if this.recent_files_filepath:
        return this.recent_files_filepath
    pattern = 'recent_files.txt'
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file == pattern:
                this.recent_files_filepath = os.path.join(root, file)
    return this.recent_files_filepath or ""


def _get_list_of_recent_files() -> list[str]:
    list_filepath = _get_recentfiles_filepath()
    if not list_filepath:
        return []

    with open(list_filepath, "r") as f:
        return f.readlines()


def _get_index_containing_text(file_lines: list[str], text_to_find: str) -> int:
    for i, l in enumerate(file_lines):
        if l.upper().find(text_to_find.upper()) > -1:
            return i
    return -1



def _delete_lines_containing_text(file_lines: list[str], text_to_find: str) -> list[str]:
    idx_to_delete = _get_index_containing_text(file_lines, text_to_find)
    while idx_to_delete > -1:
        del file_lines[idx_to_delete]
        idx_to_delete = _get_index_containing_text(file_lines, text_to_find)
    return file_lines


def _save_recent_file(recent_file: str):
    recent_file_lines = _get_list_of_recent_files()
    recent_file_lines = _delete_lines_containing_text(recent_file_lines, recent_file)
    recent_file_lines.insert(0, recent_file)
    _write_recent_files(recent_file_lines)



_save_recent_file("V:\\Inspect Programs\\Micro-Vu\\Approved Programs\\311\\Pacing\\8024077-001_REVE\\8024077-001.iwp")
_save_recent_file("V:\\Inspect Programs\\Micro-Vu\\Approved Programs\\311\\Pacing\\600130296_REV F\\600130296 BOTTOM VIEW.iwp")
_save_recent_file("V:\\Inspect Programs\\Micro-Vu\\Approved Programs\\311\\Pacing\\600130296_REV F\\600130296 END VIEW.iwp")
_save_recent_file("V:\\Inspect Programs\\Micro-Vu\\Approved Programs\\311\\Pacing\\SB-273370 REV B\\SB-273370.iwp")
_save_recent_file("V:\\Inspect Programs\\Micro-Vu\\Approved Programs\\311\\Pacing\\SA-273640 REV A\\SA-273640.iwp")
_save_recent_file("V:\\Inspect Programs\\Micro-Vu\\Approved Programs\\311\\Pacing\\PC-00293_REVB\\PC_00293.iwp")
_save_recent_file("V:\\Inspect Programs\\Micro-Vu\\Approved Programs\\311\\Pacing\\02072014-01_REVA\\02072014-01.iwp")
_save_recent_file("V:\\Inspect Programs\\Micro-Vu\\Approved Programs\\311\\Pacing\\8024077-001_REVE\\8024077-001.iwp")
_save_recent_file("V:\\Inspect Programs\\Micro-Vu\\Approved Programs\\311\\Pacing\\436656_REV A\\OP10\\436656 SIDE VIEW OP10.iwp")
_save_recent_file("V:\\Inspect Programs\\Micro-Vu\\Approved Programs\\311\\Pacing\\355965 REVB\\355965 OP10.iwp")
_save_recent_file("V:\\Inspect Programs\\Micro-Vu\\Approved Programs\\311\\Pacing\\351075-020_REVA\\351075-020 ITEM_6 CHECK.iwp")