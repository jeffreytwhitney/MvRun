import os
import glob

from abc import ABCMeta, abstractmethod


def get_processor(input_filepath: str, output_filepath: str, machine_number: str,
                  employee_id: str, job_number: str, sequence_number: str):
    return (
        CoonRapidsProcessor(input_filepath, output_filepath, machine_number, employee_id, job_number, sequence_number)
    )


def _get_node_text(line_text: str, search_value: str, start_delimiter: str, end_delimiter: str = "") -> str:
    if not end_delimiter:
        end_delimiter = start_delimiter
    title_index: int = line_text.upper().find(search_value.upper())
    begin_index: int = line_text.find(start_delimiter, title_index + len(search_value))
    end_index: int = line_text.find(end_delimiter, begin_index + 1)
    if end_index == -1:
        end_index = len(line_text)
    return line_text[begin_index + 1:end_index].strip()


def _set_node_text(line_text: str, search_value: str, set_value: str, start_delimiter: str,
                   end_delimiter: str = "") -> str:
    current_value: str = _get_node_text(line_text, search_value, start_delimiter, end_delimiter)
    current_node: str = search_value + start_delimiter + current_value + end_delimiter
    new_node: str = search_value + start_delimiter + set_value + end_delimiter
    return line_text.replace(current_node, new_node)


def _get_prompt_filepath() -> str:
    prompt_filepath: str = ""
    pattern = 'prompt_text.txt'
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == pattern:
                prompt_filepath = os.path.join(root, file)
    return prompt_filepath


def _get_prompt_lines() -> list[str]:
    prompt_filepath = _get_prompt_filepath()
    if not prompt_filepath:
        return []
    with open(prompt_filepath, "r", encoding='utf-16-le') as f:
        return f.readlines()


def _get_index_containing_text(file_lines: list[str], text_to_find: str) -> int:
    return next(
        (i for i, l in enumerate(file_lines)
         if l.upper().find(text_to_find.upper()) > 1), -1
    )


def _replace_prompt_line(file_lines: list[str], template_line: str, search_string: str, template_search_value: str, new_value: str):
    new_line = template_line.replace(template_search_value, new_value)
    if ord(new_line[0]) > 84:
        new_line = chr(84) + new_line[1:]
    if not new_line.endswith("\n"):
        new_line += "\n"

    idx = _get_index_containing_text(file_lines, search_string)
    old_line = file_lines[idx]

    if ord(old_line[0]) > 84 and old_line.startswith("Prmt", 1):
        file_lines[idx] = new_line
    elif ord(old_line[0]) == 84 and old_line.startswith("Prmt", 1):
        file_lines[idx] = new_line
    elif old_line.startswith("Prmt"):
        file_lines[idx] = new_line
    return


class Processor(metaclass=ABCMeta):
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
        self._load_data()

    @abstractmethod
    def _load_data(self):
        pass


class CoonRapidsProcessor(Processor):

    def _load_data(self):
        with open(self.input_filepath, "r", encoding='utf-16-le') as f:
            self.file_lines = f.readlines()

    def _remove_invalid_character_from_beginning_of_file(self):
        first_line = self.file_lines[0]
        first_ord = ord(first_line[0])
        if first_line.startswith("InSpec", 1):
            return
        file_start_index = first_line.find("InSpec")
        new_line = chr(first_ord) + first_line[file_start_index:]
        self.file_lines[0] = new_line

    def _replace_prompt_section(self) -> None:
        prompt_lines = _get_prompt_lines()
        for line in prompt_lines:
            if line.find("(Name \"EMPLOYEE") > -1:
                _replace_prompt_line(self.file_lines, line, "(Name \"Employee", "<E>", self.employee_id)
            if line.find("(Name \"JOB") > -1:
                _replace_prompt_line(self.file_lines, line, "(Name \"Job", "<J>", self.job_number)
            if line.find("(Name \"MACHINE") > -1:
                _replace_prompt_line(self.file_lines, line, "(Name \"Machine", "<M>", self.machine_number)
            if line.find("(Name \"SEQUENCE") > -1:
                _replace_prompt_line(self.file_lines, line, "(Name \"SEQUENCE", "<S>", self.sequence_number)

    def _get_instructions_count(self) -> str:
        return str(len([line for line in self.file_lines if line.find("(Name ") > 1]))

    def _update_instruction_count(self) -> None:
        instruction_count = self._get_instructions_count()
        idx: int = _get_index_containing_text(self.file_lines, "AutoExpFile")
        self.file_lines[idx] = _set_node_text(self.file_lines[idx], "(InsIdx", instruction_count, " ", ")")
        instruction_line_idx = next((i for i, l in enumerate(self.file_lines) if l.startswith("Instructions")), 0)
        self.file_lines[instruction_line_idx] = _set_node_text(
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
        with open(self.output_filepath, 'w+', encoding='utf-16-le', newline='\r\n') as f:
            for line in self.file_lines:
                f.write(f"{line}")

    def process_file(self) -> None:
        try:
            self._remove_invalid_character_from_beginning_of_file()
            self._replace_prompt_section()
            self._update_instruction_count()
            self._write_file_to_output_directory()

        except Exception as e:
            raise ProcessorException(e.args[0]) from e


class ProcessorException(Exception):
    pass
