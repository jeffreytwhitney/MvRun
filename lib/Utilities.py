import configparser
import os
import subprocess
import time

import win32gui


def _find_window_by_text(search_text):
    matching_windows = []

    def enum_windows_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if search_text.lower() in window_text.lower():
                matching_windows.append((hwnd, window_text))

    win32gui.EnumWindows(enum_windows_callback, None)
    return matching_windows


def _is_process_running(process_name):
    call = 'TASKLIST', '/FI', f'imagename eq {process_name}'
    output = subprocess.check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(process_name.lower())


def execute_micro_vu_program(iscmd_filepath: str, inspec_filepath, inspec_filename,
                             inspec_windowname: str, program_filepath: str):
    if not _is_process_running(inspec_filename):
        subprocess.Popen([inspec_filepath])
        time.sleep(3)
    elif windows := _find_window_by_text(inspec_windowname):
        hwnd = windows[0][0]
        win32gui.ShowWindow(hwnd, 3)
        win32gui.SetForegroundWindow(hwnd)

    subprocess.Popen([iscmd_filepath, "/run",
                      program_filepath, "/nowait"], creationflags=subprocess.SW_HIDE)


def get_ini_file_path(ini_file_name):
    current_dir = os.path.dirname(__file__)
    return current_dir + "\\" + ini_file_name + ".ini"


def get_stored_ini_value(ini_section, ini_key, ini_filename):
    ini_file_path = get_ini_file_path(ini_filename)
    config = configparser.ConfigParser()
    config.read(ini_file_path)
    try:
        config_value = config.get(ini_section, ini_key)
    except IOError:
        try:
            config_value = config.get(ini_section, "*")
        except IOError:
            config_value = ""
    return config_value


def store_ini_value(ini_value, ini_section, ini_key, ini_filename):
    try:
        ini_file_path = get_ini_file_path(ini_filename)
        if not ini_value:
            return

        config = configparser.ConfigParser()
        if not os.path.exists(ini_file_path):
            config.add_section(ini_section)
        else:
            if not config.has_section(ini_section):
                config.add_section(ini_section)
            config.read(ini_file_path)
        config.set(ini_section, ini_key, ini_value)
        with open(ini_file_path, "w") as conf:
            config.write(conf)
    except IOError:
        return


def get_unencoded_file_lines(file_path: str) -> list[str]:
    if not file_path:
        return []
    try:
        with open(file_path, "r") as f:
            return f.readlines()
    except IOError:
        return []


def get_utf_encoded_file_lines(file_path: str) -> list[str]:
    if not file_path:
        return []
    try:
        with open(file_path, "r", encoding='utf-16-le') as f:
            return f.readlines()
    except IOError:
        return []


def get_filepath_by_name(file_name: str) -> str:
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == file_name:
                return os.path.join(root, file)
    return ""


def get_file_as_string(file_path: str):
    try:
        with open(file_path, "r") as f:
            return str(f.read())
    except IOError:
        return ""


def write_lines_to_file(output_filepath: str, file_lines: list[str], encoding='utf-8', newline='\n'):
    try:
        with open(output_filepath, 'w+', encoding=f'{encoding}', newline=f'{newline}') as f:
            for line in file_lines:
                f.write(f"{line}")
    except IOError:
        return
