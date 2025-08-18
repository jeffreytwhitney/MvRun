from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
import re
from lib.Utilities import get_utf_encoded_file_lines


class InstructionType(StrEnum):
    COMMAND_LINE = 'CmdLn'
    TEXT = 'Txt'
    PROMPT = 'Prmt'
    POINT = 'Pnt'
    SYSTEM = 'Sys'
    LINE = 'Lin'
    ARC = 'Arc'
    CALCULATOR = 'Calc'
    CIRCLE = 'Crc'
    DISTANCE = 'Dst'
    CLOSEDSPLINE = 'CSpl'
    OPENSPLINE = 'OSpl'
    ANGLE = 'Ang'
    GAP = 'Gap'
    PLANE = 'Pln'
    POINTCLOUD = 'PtCld'
    SLOT = "Slt"
    RECTANGLE = "Rec"
    ORING = "ORn"


@dataclass
class Instruction:
    line_index: int
    guid: str
    text: str
    name: str
    type: InstructionType


class MicroVuException(Exception):
    pass


class MicroVuProgram:
    _filepath: str
    _is_smartprofile: bool
    _file_lines: list[str]
    _instructions: list[Instruction]
    _is_setup: bool = False

    # Static Methods
    @staticmethod
    def get_node(line_text: str, search_value: str) -> str:
        begin_index: int = line_text.upper().find(f"({search_value.upper()}")
        end_index: int = line_text.find(")", begin_index + len(search_value) + 1)
        if end_index == -1:
            end_index = len(line_text)
        return line_text[begin_index:end_index + 1].strip()

    @staticmethod
    def get_node_text(line_text: str, search_value: str, start_delimiter: str, end_delimiter: str = "") -> str:
        if not end_delimiter:
            end_delimiter = start_delimiter
        title_index: int = line_text.upper().find(search_value.upper())
        begin_index: int = line_text.find(start_delimiter, title_index + len(search_value))
        end_index: int = line_text.find(end_delimiter, begin_index + 1)
        if end_index == -1:
            end_index = len(line_text)
        return line_text[begin_index + 1:end_index].strip()

    @staticmethod
    def set_node_text(line_text: str, search_value: str, set_value: str, start_delimiter: str,
                      end_delimiter: str = "") -> str:
        current_value: str = MicroVuProgram.get_node_text(line_text, search_value, start_delimiter, end_delimiter)
        current_node: str = search_value + start_delimiter + current_value + end_delimiter
        new_node: str = search_value + start_delimiter + set_value + end_delimiter
        return line_text.replace(current_node, new_node)

    # Dunder Methods
    def __init__(self, input_filepath: str):
        self._filepath = input_filepath
        self._file_lines = get_utf_encoded_file_lines(self._filepath)
        self._load_instructions()

    # Internal Methods
    def _get_instructions_count(self) -> int:
        return len([line for line in self._file_lines if line.find("(Name ") > 1])

    def _global_replace(self, old_value: str, new_value: str) -> None:
        quoted_old_value = f"\"{old_value}\""
        quoted_new_value = f"\"{new_value}\""
        for i, l in enumerate(self._file_lines):
            if l.find(quoted_old_value) > 0:
                new_line = l.replace(quoted_old_value, quoted_new_value)
                self._file_lines[i] = new_line

    def _load_instructions(self) -> None:
        pattern = r'^(\w+)\s+\w+\s+(\w+)\s+\(Name\s+"([^"]+)"\)'
        instruction_lines = []

        for index, line in enumerate(self._file_lines):
            if line.find("(Name ") > 1:
                instruction_type_text = re.search(pattern, line)[1]
                instruction_type = InstructionType(instruction_type_text)
                guid = re.search(pattern, line)[2]
                name_value = re.search(pattern, line)[3]
                instruction = Instruction(index, guid, line, name_value, instruction_type)
                instruction_lines.append(instruction)

        self._instructions = instruction_lines

    # Properties
    @property
    def export_filepath(self) -> str:
        if self.is_smartprofile:
            return "C:\\TEXT\\OUTPUT.txt"
        if line_idx := self.get_index_containing_text("AutoExpFile"):
            return MicroVuProgram.get_node_text(self._file_lines[line_idx], "AutoExpFile", "\"")
        else:
            return ""

    @export_filepath.setter
    def export_filepath(self, value: str) -> None:
        if self.is_smartprofile:
            value = "C:\\TEXT\\OUTPUT.txt"
        line_idx = self.get_index_containing_text("AutoExpFile")
        if not line_idx:
            return
        line_text = self._file_lines[line_idx]
        updated_line_text = MicroVuProgram.set_node_text(line_text, "(ExpFile ", value, "\"")
        updated_line_text = MicroVuProgram.set_node_text(updated_line_text, "(AutoExpFile ", value, "\"")
        if self.is_smartprofile:
            updated_line_text = updated_line_text.replace("(AutoExpFSApSt DT)", "(AutoExpFSApSt None)")
        else:
            updated_line_text = updated_line_text.replace("(AutoExpFSApSt None)", "(AutoExpFSApSt DT)")
        updated_line_text = updated_line_text.replace("(FldDlm Tab)", "(FldDlm CrLf)")
        updated_line_text = updated_line_text.replace("(FldDlm Comma)", "(FldDlm CrLf)")
        updated_line_text = updated_line_text.replace("(NoDblQt 1)", "(NoDblQt 0)")
        updated_line_text = updated_line_text.replace("(RunSep 1)", "(RunSep 0)")
        updated_line_text = updated_line_text.replace("(ValDlm Comma)", "(ValDlm Tab)")
        updated_line_text = updated_line_text.replace("(AutoRptTemplateName \"\")", "(AutoRptTemplateName \"Classic\")")

        if self._is_setup and not self.is_smartprofile:
            updated_line_text = updated_line_text.replace("(AutoExpFileInf ((Enab 1)", "(AutoExpFileInf ((Enab 0)")

        self._file_lines[line_idx] = updated_line_text

    @property
    def file_lines(self) -> list[str]:
        return self._file_lines

    @property
    def filepath(self) -> str:
        return self._filepath

    @property
    def filename(self) -> str:
        return Path(self._filepath).name

    @property
    def has_setup_picture(self) -> bool:
        insertion_index = self.prompt_insertion_index - 2
        command_lines = self.get_instructions_by_type(InstructionType.COMMAND_LINE)
        return any(
            line.line_index <= insertion_index
            and line.text.lower().find(".jpg") > -1
            for line in command_lines
        )

    @property
    def instructions_count(self) -> int:
        return self._get_instructions_count()

    @property
    def instructions_index(self) -> int:
        return next((i for i, l in enumerate(self._file_lines) if l.startswith("Instructions")), 0)

    @property
    def is_file_salted(self) -> bool:
        return self._file_lines[0].startswith("InSpec") is False

    @property
    def is_multi_part(self):
        return self.sequence_count > 1

    @property
    def is_setup(self):
        return self._is_setup

    @is_setup.setter
    def is_setup(self, value: bool):
        self._is_setup = value

    @property
    def is_smartprofile(self) -> bool:
        line_idx = self.get_index_containing_text("AutoExpFile")
        existing_export_filepath = str(Path(MicroVuProgram.get_node_text(
            self.file_lines[line_idx], "AutoExpFile", "\""))).upper()
        existing_export_filename = Path(MicroVuProgram.get_node_text(
            self.file_lines[line_idx], "AutoExpFile", "\"")).stem.upper()
        if existing_export_filename == "OUTPUT":
            return True
        return "C:\\MICROVU\\POINTCLOUDS\\" in existing_export_filepath

    @property
    def prompt_insertion_index(self) -> int:
        insert_index: int = self.get_index_containing_text("(Name \"Created")
        if not insert_index or not self._file_lines[insert_index].startswith("Txt"):
            return -1

        temp_idx: int = self.get_index_containing_text("(Name \"Edited")
        if not temp_idx or not self._file_lines[temp_idx].startswith("Txt"):
            return -1
        return max(temp_idx, insert_index)

    @property
    def sequence_count(self) -> int:
        return sum("(NAME \"SEQUENCE" in line.upper() for line in self._file_lines)

    # Public Methods
    def delete_line_containing_text(self, text_to_find: str) -> None:
        idx_to_delete = self.get_index_containing_text(text_to_find)
        if idx_to_delete > 0:
            del self._file_lines[idx_to_delete]
            self._load_instructions()

    def get_index_containing_text(self, text_to_find: str) -> int:
        return next(
            (i for i, l in enumerate(self._file_lines)
             if l.upper().find(text_to_find.upper()) > 1), -1
        )

    def get_instructions_by_name(self, instruction_name: str) -> list[Instruction]:
        return [i for i in self._instructions if i.name.lower().find(instruction_name.lower()) > -1]

    def get_instructions_by_name_and_type(self, instruction_name: str, instruction_type: InstructionType):
        return [i for i in self._instructions if i.name.lower().find(instruction_name.lower()) > -1 and instruction_type == i.type]

    def get_instructions_by_type(self, instruction_type: InstructionType):
        return [i for i in self._instructions if i.type == instruction_type]

    def get_line_containing_text(self, text_to_find: str) -> str:
        idx = self.get_index_containing_text(text_to_find)
        return self._file_lines[idx] if idx > -1 else ""

    def insert_line(self, line_index: int, line: str) -> None:
        self._file_lines.insert(line_index, line)
        self._load_instructions()

    def update_instruction_count(self) -> None:
        instruction_count = str(self._get_instructions_count())
        idx: int = self.get_index_containing_text("AutoExpFile")
        self._file_lines[idx] = MicroVuProgram.set_node_text(
            self._file_lines[idx], "(InsIdx", instruction_count, " ", ")")
        instruction_line_idx = next((i for i, l in enumerate(self._file_lines) if l.startswith("Instructions")), 0)
        self._file_lines[instruction_line_idx] = MicroVuProgram.set_node_text(
            self._file_lines[instruction_line_idx], "Instructions", instruction_count, " ")

    def unsalt_file(self) -> None:
        first_line = self._file_lines[0]
        first_ord = ord(first_line[0])
        if first_line.startswith("InSpec", 1):
            return
        file_start_index = first_line.find("InSpec")
        new_line = chr(first_ord) + first_line[file_start_index:]
        self._file_lines[0] = new_line
