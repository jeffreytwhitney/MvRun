import glob
import os
from abc import ABCMeta

from lib import Utilities
from lib.Utilities import get_utf_encoded_file_lines, write_lines_to_file


def get_processor(input_filepath: str, output_filepath: str, machine_number: str,
                  employee_id: str, job_number: str, sequence_number: str):
    return (
            CoonRapidsProcessor(input_filepath, output_filepath, machine_number, employee_id, job_number, sequence_number)
    )


class Processor(metaclass=ABCMeta):
    _file_lines: list[str]

    def __init__(self, input_filepath: str, output_filepath: str, machine_number: str,
                 employee_id: str, job_number: str, sequence_number: str):
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath
        self.output_directory = os.path.dirname(self.output_filepath)
        self.output_directory_searchpath = f"{self.output_directory}//*.iwp"
        self.machine_number = machine_number
        self.employee_id = employee_id
        self.job_number = job_number
        self.sequence_number = sequence_number
        self._file_lines = get_utf_encoded_file_lines(input_filepath)

    @staticmethod
    def _get_node_text(line_text: str, search_value: str, start_delimiter: str, end_delimiter: str = "") -> str:
        if not end_delimiter:
            end_delimiter = start_delimiter
        title_index: int = line_text.upper().find(search_value.upper())
        begin_index: int = line_text.find(start_delimiter, title_index + len(search_value))
        end_index: int = line_text.find(end_delimiter, begin_index + 1)
        if end_index == -1:
            end_index = len(line_text)
        return line_text[begin_index + 1:end_index].strip()

    @staticmethod
    def _set_node_text(line_text: str, search_value: str, set_value: str, start_delimiter: str,
                       end_delimiter: str = "") -> str:
        current_value: str = Processor._get_node_text(line_text, search_value, start_delimiter, end_delimiter)
        current_node: str = search_value + start_delimiter + current_value + end_delimiter
        new_node: str = search_value + start_delimiter + set_value + end_delimiter
        return line_text.replace(current_node, new_node)

    @staticmethod
    def _get_prompt_filepath() -> str:
        prompt_filepath: str = ""
        pattern = 'prompt_text.txt'
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file == pattern:
                    prompt_filepath = os.path.join(root, file)
        return prompt_filepath

    @staticmethod
    def _get_prompt_lines() -> list[str]:
        prompt_filepath = Processor._get_prompt_filepath()
        if not prompt_filepath:
            return []
        with open(prompt_filepath, "r", encoding='utf-16-le') as f:
            return f.readlines()

    @staticmethod
    def _get_index_containing_text(file_lines: list[str], text_to_find: str) -> int:
        return next(
                (i for i, l in enumerate(file_lines)
                 if l.upper().find(text_to_find.upper()) > 1), -1
        )

    @staticmethod
    def _insert_line_at_index(file_lines: list[str], idx: int, new_line: str) -> None:
        file_lines.insert(idx, new_line)

    @staticmethod
    def _replace_prompt_line(file_lines: list[str],
                             template_line: str, search_string: str, template_search_value: str, new_value: str):
        new_line = template_line.replace(template_search_value, new_value)
        if ord(new_line[0]) > 84:
            new_line = chr(84) + new_line[1:]
        if not new_line.endswith("\n"):
            new_line += "\n"

        idx = Processor._get_index_containing_text(file_lines, search_string)
        old_line = file_lines[idx]

        if ord(old_line[0]) > 84 and old_line.startswith("Prmt", 1):
            file_lines[idx] = new_line
        elif ord(old_line[0]) == 84 and old_line.startswith("Prmt", 1):
            file_lines[idx] = new_line
        elif old_line.startswith("Prmt"):
            file_lines[idx] = new_line
        return

    @property
    def file_lines(self) -> list[str]:
        return self._file_lines

    @property
    def _is_smart_profile(self) -> bool:
        return any(
            (i for i, l in enumerate(self.file_lines)
             if l.upper().find("OUTPUT.TXT") > 0)
        )

    @property
    def _should_change_export_path(self) -> bool:
        if self._is_smart_profile:
            return False
        change_export_paths = Utilities.get_stored_ini_value("ProcessSwitches", "change_export_path", "Settings")
        return int(change_export_paths) == 1

    @property
    def _prompt_insertion_index(self) -> int:
        insert_index: int = self._get_index_containing_text(self.file_lines, "(Name \"Created")
        if not insert_index or not self.file_lines[insert_index].startswith("Txt"):
            return -1

        temp_idx: int = self._get_index_containing_text(self.file_lines, "(Name \"Edited")
        if not temp_idx or not self.file_lines[temp_idx].startswith("Txt"):
            return -1
        return max(temp_idx, insert_index)


class CoonRapidsProcessor(Processor):

    def _remove_invalid_character_from_beginning_of_file(self):
        first_line = self.file_lines[0]
        first_ord = ord(first_line[0])
        if first_line.startswith("InSpec", 1):
            return
        file_start_index = first_line.find("InSpec")
        new_line = chr(first_ord) + first_line[file_start_index:]
        self.file_lines[0] = new_line

    def _replace_prompt_section(self) -> None:
        prompt_lines = CoonRapidsProcessor._get_prompt_lines()
        for line in prompt_lines:
            if line.find("(Name \"SETUP_PROMPT") > -1:
                insertion_index: int = self._prompt_insertion_index
                CoonRapidsProcessor._insert_line_at_index(self.file_lines, insertion_index, line)
            if line.find("(Name \"EMPLOYEE") > -1:
                CoonRapidsProcessor._replace_prompt_line(self.file_lines, line, "(Name \"Employee", "<E>", self.employee_id)
            if line.find("(Name \"JOB") > -1:
                CoonRapidsProcessor._replace_prompt_line(self.file_lines, line, "(Name \"Job", "<J>", self.job_number)
            if line.find("(Name \"MACHINE") > -1:
                CoonRapidsProcessor._replace_prompt_line(self.file_lines, line, "(Name \"Machine", "<M>", self.machine_number)
            if line.find("(Name \"SEQUENCE") > -1:
                CoonRapidsProcessor._replace_prompt_line(self.file_lines, line, "(Name \"SEQUENCE", "<S>", self.sequence_number)

    def _replace_export_path(self):
        line_idx = Processor._get_index_containing_text(self.file_lines, "AutoExpFile")
        if not line_idx:
            return
        line_text = self.file_lines[line_idx]
        current_file_path = Processor._get_node_text(line_text, "AutoExpFile", "\"")
        current_file_name = os.path.basename(current_file_path)
        export_root_path = Utilities.get_stored_ini_value("Paths", "export_rootpath", "Settings")
        new_export_path = os.path.join(export_root_path, current_file_name)
        updated_line_text = Processor._set_node_text(line_text, "(ExpFile ", new_export_path, "\"")
        updated_line_text = Processor._set_node_text(updated_line_text, "(AutoExpFile ", new_export_path, "\"")
        self.file_lines[line_idx] = updated_line_text

    def _get_instructions_count(self) -> str:
        return str(len([line for line in self.file_lines if line.find("(Name ") > 1]))

    def _update_instruction_count(self) -> None:
        instruction_count = self._get_instructions_count()
        idx: int = CoonRapidsProcessor._get_index_containing_text(self.file_lines, "AutoExpFile")
        self.file_lines[idx] = CoonRapidsProcessor._set_node_text(
                self.file_lines[idx], "(InsIdx", instruction_count, " ", ")")
        instruction_line_idx = next((i for i, l in enumerate(self.file_lines) if l.startswith("Instructions")), 0)
        self.file_lines[instruction_line_idx] = CoonRapidsProcessor._set_node_text(
                self.file_lines[instruction_line_idx], "Instructions", instruction_count, " ")
        return

    def _delete_all_microvu_files(self):
        files = glob.glob(self.output_directory_searchpath)
        for f in files:
            os.remove(f)

    def _write_file_to_output_directory(self):
        if not os.path.exists(self.output_directory):
            os.mkdir(self.output_directory)
        self._delete_all_microvu_files()
        write_lines_to_file(self.output_filepath, self.file_lines, encoding='utf-16-le', newline='\r\n')

    def process_file(self) -> None:
        try:
            self._remove_invalid_character_from_beginning_of_file()
            if self._should_change_export_path:
                self._replace_export_path()
            self._replace_prompt_section()
            self._update_instruction_count()
            self._write_file_to_output_directory()

        except Exception as e:
            raise ProcessorException(e.args[0]) from e


class ProcessorException(Exception):
    pass
