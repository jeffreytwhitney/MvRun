import configparser
import os
import subprocess
import time


def is_process_running(process_name):
    call = 'TASKLIST', '/FI', f'imagename eq {process_name}'
    output = subprocess.check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(process_name.lower())


def start_application(exe_filepath: str):
    os.startfile(exe_filepath)
    time.sleep(3)


def get_ini_file_path(ini_file_name):
    current_dir = os.path.dirname(__file__)
    return current_dir + "\\" + ini_file_name + ".ini"


def get_stored_ini_value(ini_section, ini_key, ini_filename):
    ini_file_path = get_ini_file_path(ini_filename)
    config = configparser.ConfigParser()
    config.read(ini_file_path)
    try:
        config_value = config.get(ini_section, ini_key)
    except:
        try:
            config_value = config.get(ini_section, "*")
        except:
            config_value = ""
    return config_value


def store_ini_value(ini_value, ini_section, ini_key, ini_filename):
    ini_file_path = get_ini_file_path(ini_filename)
    config = configparser.ConfigParser()
    if not os.path.exists(ini_file_path):
        config.add_section(ini_section)
        config.set(ini_section, ini_key, ini_value)
        with open(ini_file_path, "w") as conf:
            config.write(conf)
    else:
        if not config.has_section(ini_section):
            config.add_section(ini_section)
        config.read(ini_file_path)
        config.set(ini_section, ini_key, ini_value)
        with open(ini_file_path, "w") as conf:
            config.write(conf)


def get_unencoded_file_lines(file_path: str) -> list[str]:
    if not file_path:
        return []
    with open(file_path, "r") as f:
        return f.readlines()


def get_utf_encoded_file_lines(file_path: str) -> list[str]:
    if not file_path:
        return []
    with open(file_path, "r", encoding='utf-16-le') as f:
        return f.readlines()


def get_filepath_by_name(file_name: str) -> str:
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == file_name:
                return os.path.join(root, file)
    return ""


def get_file_as_string(file_path: str):
    with open(file_path, "r") as f:
        return str(f.read())


def write_lines_to_file(output_filepath: str, file_lines: list[str], encoding='utf-8', newline='\n'):
    with open(output_filepath, 'w+', encoding=f'{encoding}', newline=f'{newline}') as f:
        for line in file_lines:
            f.write(f"{line}")
