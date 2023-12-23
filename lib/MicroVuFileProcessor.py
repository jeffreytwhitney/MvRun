import os

from abc import ABCMeta, abstractmethod


def get_processor(input_filepath: str, op_num: str, user_initials: str, output_filepath: str, rev_number: str,
                  smartprofile_file_name: str, is_profile: bool):
    return (
        CoonRapidsProcessor(input_filepath, op_num, user_initials, output_filepath, rev_number, smartprofile_file_name, is_profile)
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


class Processor(metaclass=ABCMeta):
    def __init__(self, mv_input_filepath: str, op_num: str, user_initials: str, mv_output_filepath: str,
                 rev_number: str, smartprofile_file_name: str, is_profile: bool):
        self.filepath = mv_input_filepath
        self.user_initials = user_initials
        self.input_filepath = mv_input_filepath
        self.output_filepath = mv_output_filepath
        self.smartprofile_filepath = smartprofile_file_name
        self.op_number = op_num
        self.is_profile = is_profile
        self.rev_number = rev_number
        self._load_data()

    @abstractmethod
    def _load_data(self):
        pass


class CoonRapidsProcessor(Processor):

    def _load_data(self):
        with open(self.filepath, "r", encoding='utf-16-le') as f:
            self.file_lines = f.readlines()

    def _get_index_containing_text(self, text_to_find: str) -> int:
        return next((i for i, l in enumerate(self.file_lines) if l.upper().find(text_to_find.upper()) > 1), 0)

    def _replace_prompt_section(self) -> None:
        prompt_filepath: str = ""
        insert_index: int = self._get_index_containing_text("(Name \"Created")
        if not insert_index or not self.file_lines[insert_index].startswith("Txt"):
            raise ProcessorException("There is no 'Created By' line. Cannot process file.")
        temp_idx: int = self._get_index_containing_text("(Name \"Edited")
        if not temp_idx or not self.file_lines[temp_idx].startswith("Txt"):
            raise ProcessorException("There is no 'Edited By' line. Cannot process file.")
        if temp_idx > insert_index:
            insert_index = temp_idx
        insert_index += 1
        pattern = 'sp_prompt_text.txt' if self.is_profile else 'prompt_text.txt'
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file == pattern:
                    prompt_filepath = os.path.join(root, file)
        if not prompt_filepath:
            return
        with open(prompt_filepath, "r", encoding='utf-16-le') as f:
            prompt_lines = f.readlines()

        return

    def _get_instructions_count(self) -> str:
        return str(len([line for line in self.file_lines if line.find("(Name ") > 1]))

    def _update_instruction_count(self) -> None:
        instruction_count = self._get_instructions_count()
        idx: int = self._get_index_containing_text("AutoExpFile")
        self.file_lines[idx] = _set_node_text(self.file_lines[idx], "(InsIdx", instruction_count, " ", ")")
        instruction_line_idx = next((i for i, l in enumerate(self.file_lines) if l.startswith("Instructions")), 0)
        self.file_lines[instruction_line_idx] = _set_node_text(
            self.file_lines[instruction_line_idx], "Instructions", instruction_count, " ")
        return

    def process_file(self) -> None:
        try:
            self._replace_prompt_section()
            self._update_instruction_count()
            if os.path.exists(self.output_filepath):
                os.remove(self.output_filepath)
            file_directory = os.path.dirname(self.output_filepath)
            if not os.path.exists(file_directory):
                os.mkdir(file_directory)
            with open(self.output_filepath, 'w+', encoding='utf-16-le', newline='\r\n') as f:
                for line in self.file_lines:
                    f.write(f"{line}")
        except Exception as e:
            raise ProcessorException(e.args[0]) from e


class ProcessorException(Exception):
    pass
