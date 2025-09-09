import glob
import os
from abc import ABCMeta

from typing_extensions import evaluate_forward_ref
from win32com.makegw.makegwparse import error_not_found

from lib import Utilities
from lib.MicroVuProgram import MicroVuProgram
from lib.Utilities import write_lines_to_file
from logging import Logger
from lib import MvLogger


def get_processor(input_filepath: str, is_setup: bool, machine_name: str, employee_id: str,
                  job_number: str, sequence_numbers: list[int], output_path: str):
    return (CoonRapidsProcessor(input_filepath, is_setup, machine_name, employee_id,
                                job_number, sequence_numbers, output_path))


class Processor(metaclass=ABCMeta):
    _file_lines: list[str]
    _machine_number: str
    _employee_id: str
    _job_number: str
    _sequence_numbers: list[int]
    _is_setup: bool = False
    _microvu_program: MicroVuProgram
    _output_filepath: str
    _output_directory: str
    _output_directory_searchpath: str
    _logger: Logger

    # Dunder Methods
    def __init__(self, input_filepath: str, is_setup: bool, machine_name: str, employee_id: str, job_number: str,
                 sequence_numbers: list[int], output_path: str):
        self._logger = MvLogger.get_logger("microVuFileProcessorLogger")
        self.input_filepath = input_filepath
        self._microvu_program = MicroVuProgram(input_filepath)
        self._output_filepath = output_path
        self._output_directory = os.path.dirname(self._output_filepath)
        self._output_directory_searchpath = f"{self._output_directory}//*.iwp"
        self._is_setup = is_setup
        self._machine_number = machine_name
        self._employee_id = employee_id
        self._job_number = job_number
        self._sequence_numbers = sequence_numbers

    # Status Methods
    @staticmethod
    def _get_eof_file_path() -> str:
        prompt_filepath: str = ""
        pattern = 'eof_text.txt'
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file == pattern:
                    prompt_filepath = os.path.join(root, file)
        return prompt_filepath

    @staticmethod
    def _get_eof_file_lines() -> list[str]:
        eof_filepath = Processor._get_eof_file_path()
        if not eof_filepath:
            return []
        with open(eof_filepath, "r", encoding='utf-16-le') as f:
            return f.readlines()

    @staticmethod
    def _get_prompt_file_path() -> str:
        prompt_filepath: str = ""
        pattern = 'prompt_text.txt'
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file == pattern:
                    prompt_filepath = os.path.join(root, file)
        return prompt_filepath

    @staticmethod
    def _get_prompt_file_lines() -> list[str]:
        prompt_filepath = Processor._get_prompt_file_path()
        if not prompt_filepath:
            return []
        with open(prompt_filepath, "r", encoding='utf-16-le') as f:
            return f.readlines()

    # Protected Methods
    def _delete_all_microvu_files(self):
        files = glob.glob(self._output_directory_searchpath)
        for f in files:
            os.remove(f)

    def _insert_eof_section(self) -> None:
        eof_lines = self._get_eof_file_lines()
        eof_batch_filepath = Utilities.get_stored_ini_value("Paths", "local_eof_batch_file", "Settings")
        microvu_system_id = self._microvu_program.last_microvu_system_id
        exe_line = eof_lines[1]
        exe_line = exe_line.replace("<?SYS>", microvu_system_id)
        exe_line = exe_line.replace("<?EXE>", eof_batch_filepath)
        self._logger.debug(f"_insert_eof_section: Inserted EOF at index {self._microvu_program.instructions_index}")
        self._microvu_program.file_lines.append(exe_line)
        self._microvu_program.file_lines.append(eof_lines[2])
        self._microvu_program.file_lines.append(eof_lines[3])

    def _replace_prompt_section(self) -> None:
        prompt_lines = self._get_prompt_file_lines()
        for line in prompt_lines:
            if line.find("(Name \"SETUP_PROMPT") > -1 and self._should_insert_prompt:
                insertion_index: int = self._microvu_program.prompt_insertion_index
                self._microvu_program.insert_line(insertion_index, line)
                self._logger.debug(f"_replace_prompt_section: Inserted prompt at index {insertion_index}")
                continue

            if line.find("(Name \"EMPLOYEE") > -1:
                new_line = line.replace("<E>", self.employee_id)
                if microvu_employee_prompt := self._microvu_program.get_instructions_by_name("EMPLOYEE")[0]:
                    self._microvu_program.file_lines[microvu_employee_prompt.line_index] = new_line
                    self._logger.debug(f"_replace_prompt_section: Replaced employee prompt with {new_line}")   
                    continue

            if line.find("(Name \"JOB") > -1:
                new_line = line.replace("<J>", self.job_number)
                if microvu_job_prompt := self._microvu_program.get_instructions_by_name("JOB")[0]:
                    self._microvu_program.file_lines[microvu_job_prompt.line_index] = new_line
                    self._logger.debug(f"_replace_prompt_section: Replaced job prompt with {new_line}")   
                    continue

            if line.find("(Name \"MACHINE") > -1:
                new_line = line.replace("<M>", self.machine_number)
                if microvu_machine_prompt := self._microvu_program.get_instructions_by_name("MACHINE")[0]:
                    self._microvu_program.file_lines[microvu_machine_prompt.line_index] = new_line
                    self._logger.debug(f"_replace_prompt_section: Replaced machine prompt with {new_line}")   
                    continue

            if line.find("(Name \"SEQUENCE") > -1:
                if len(self.sequence_numbers) == 1:
                    new_line = line.replace("<S>", str(self.sequence_numbers[0]))
                    new_line = new_line.replace("<I>", "")
                    if microvu_sequence_prompt := self._microvu_program.get_instructions_by_name("SEQUENCE")[0]:
                        self._microvu_program.file_lines[microvu_sequence_prompt.line_index] = new_line
                        self._logger.debug(f"_replace_prompt_section: Replaced single-part sequence prompt with {new_line}")   
                    continue
                elif len(self.sequence_numbers) > 1:
                    sequence_prompts = self._microvu_program.get_instructions_by_name("SEQUENCE")
                    for counter, sequence_number in enumerate(self.sequence_numbers, start=1):
                        new_line = line.replace("<S>", str(sequence_number))
                        new_line = new_line.replace("<I>", str(counter))
                        if microvu_sequence_prompt := sequence_prompts[counter - 1]:
                            self._microvu_program.file_lines[microvu_sequence_prompt.line_index] = new_line
                            self._logger.debug(f"_replace_prompt_section: Replaced multi-part sequence prompt {counter} with {new_line}")   
                    continue

    def _write_file_to_output_directory(self):
        if not os.path.exists(self._output_directory):
            os.mkdir(self._output_directory)
        self._delete_all_microvu_files()
        write_lines_to_file(self._output_filepath, self._microvu_program.file_lines, encoding='utf-16-le', newline='\r\n')
        self._logger.debug(f"_write_file_to_output_directory: Wrote file to {self._output_filepath}")

    # Public Methods
    def add_sequence_number(self, sequence_number: int):
        self._sequence_numbers.append(sequence_number)

    def process_file(self) -> None:
        raise NotImplementedError("Must be implemented by subclass")

    # Public Properties
    @property
    def sequence_numbers(self) -> list[int]:
        return self._sequence_numbers

    @property
    def employee_id(self) -> str:
        return self._employee_id

    @employee_id.setter
    def employee_id(self, value: str):
        self._employee_id = value

    @property
    def is_setup(self):
        return self._is_setup

    @property
    def job_number(self) -> str:
        return self._job_number

    @property
    def machine_number(self) -> str:
        return self._machine_number

    @property
    def microvu_program(self) -> MicroVuProgram:
        return self._microvu_program

    # Protected Properties
    @property
    def _should_change_export_path(self) -> bool:
        if self._microvu_program.is_smartprofile:
            return False
        change_export_paths = Utilities.get_stored_ini_value("ProcessSwitches", "change_export_path", "Settings")
        return int(change_export_paths) == 1
    
    @property
    def _should_insert_prompt(self) -> bool:
        insert_prompt = Utilities.get_stored_ini_value("ProcessSwitches", "insert_prompt", "Settings")
        return int(insert_prompt) == 1


class CoonRapidsProcessor(Processor):
    def process_file(self) -> None:
        if len(self._sequence_numbers) != self._microvu_program.sequence_count:
            self._logger.error("Sequence count does not match number of sequences in file.")
            raise ProcessorException("Sequence count does not match number of sequences in file.")

        try:
            self._process_microvu()
        except Exception as e:
            if e.args[0] is not None:
                self._logger.error(f"Error occurred:'{e.args[0]}'.")
                raise ProcessorException(e.args[0]) from e

    def _process_microvu(self):
        self._microvu_program.is_setup = self.is_setup
        self._microvu_program.unsalt_file()
        if self.is_setup:
            self._microvu_program.export_filepath = ""
        elif self._should_change_export_path:
            export_root_path = Utilities.get_stored_ini_value("Paths", "export_rootpath", "Settings")
            existing_export_path = self._microvu_program.export_filepath[3:]
            new_export_path = os.path.join(export_root_path, existing_export_path)
            self._microvu_program.export_filepath = new_export_path
        self._replace_prompt_section()
        self._insert_eof_section()
        self._microvu_program.update_instruction_count()
        self._write_file_to_output_directory()


class ProcessorException(Exception):
    pass
