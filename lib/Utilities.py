import configparser
import os


def GetIniFilePath(ini_file_name):
    current_dir = os.path.dirname(__file__)
    ini_path = current_dir + "\\" + ini_file_name + ".ini"
    return ini_path


def GetStoredIniValue(ini_section, ini_key, ini_filename):
    ini_file_path = GetIniFilePath(ini_filename)
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


def StoreIniValue(ini_value, ini_section, ini_key, ini_filename):
    ini_file_path = GetIniFilePath(ini_filename)
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


def GetMicroVuFolderSubDirectory(directory_to_check):
    if directory_to_check.find("\\311\\") != -1:
        return "311"
    if directory_to_check.find("\\341\\") != -1:
        return "341"
    if directory_to_check.find("\\420\\") != -1:
        return "420"
