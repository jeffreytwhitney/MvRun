import os

from lib.MicroVuProgram import MicroVuProgram


def test_static_node_helpers():
    line = 'CmdLn 1 AAA (Name "AutoExport") (AutoExpFile "M:\\DATA\\FILE.csv")'
    # get_node
    node = MicroVuProgram.get_node(line, "AutoExpFile")
    assert node == '(AutoExpFile "M:\\DATA\\FILE.csv")'
    # get_node_text
    text = MicroVuProgram.get_node_text(line, "AutoExpFile", '"')
    assert text == r"M:\DATA\FILE.csv"
    # set_node_text
    updated = MicroVuProgram.set_node_text(line, "(AutoExpFile ", r"D:\OUT\res.csv", '"')
    assert '(AutoExpFile "D:\\OUT\\res.csv")' in updated


def test_parsing_and_properties_non_smartprofile(mv_rotary_path):
    micro_vu = MicroVuProgram(mv_rotary_path)
    bob = micro_vu.file_lines[0]
    assert micro_vu.file_lines[0].startswith("\ufeff#")
    assert micro_vu.filepath == mv_rotary_path
    assert micro_vu.filename == os.path.basename(mv_rotary_path)
    assert micro_vu.is_smartprofile is False
    assert r"Z:\2030-6516-1300_OP10_REVB_.csv" in micro_vu.export_filepath
    assert micro_vu.instructions_index == 3
    assert micro_vu.is_file_salted is True
    assert micro_vu.instructions_count == 140
    assert micro_vu.has_rotary is True
    assert micro_vu.has_eof_batch_call is False
    assert micro_vu.sequence_count == 1
    assert micro_vu.is_multi_part is False
    assert micro_vu.prompt_insertion_index == 11
    assert micro_vu.has_setup_picture is True
    assert micro_vu.last_microvu_system_id == "E91A378"
    micro_vu.unsalt_file()
    assert micro_vu.file_lines[0].startswith("\ufeffInSpec")
    assert micro_vu.is_file_salted is False


def test_export_filepath_setter_non_smartprofile_updates_flags(salted_path):
    prog = MicroVuProgram(salted_path)

    new_out = r"D:\EXPORTS\out.csv"
    prog.export_filepath = new_out

    line_idx = prog.get_index_containing_text("AutoExpFile")
    line = prog.file_lines[line_idx]

    assert f'(AutoExpFile "{new_out}")' in line
    assert "(FldDlm CrLf)" in line
    assert "(AutoConf 0)" in line
    assert "(NoDblQt 0)" in line
    assert "(RunSep 0)" in line
    assert "(ValDlm Tab)" in line
    assert '(AutoRptTemplateName "Classic")' in line


def test_sequence_count_and_is_multi_part(mv_multipart_path):
    prog = MicroVuProgram(mv_multipart_path)
    assert prog.sequence_count == 5
    assert prog.is_multi_part is True


def test_unsalted(unsalted_path):
    prog = MicroVuProgram(unsalted_path)
    assert prog.is_file_salted is False


def test_delete_insert_and_update_instruction_count(unsalted_path):
    prog = MicroVuProgram(unsalted_path)

    assert prog.instructions_count == 57
    prog.delete_line_containing_text('(Name "EMPLOYEE")')
    assert prog.instructions_count == 56

    insert_at = prog.instructions_index + 1
    prog.insert_line(insert_at, 'Txt 1 NEW1 (Name "INSERTED") something')
    assert prog.instructions_count == 57

    prog.update_instruction_count()

    auto_idx = prog.get_index_containing_text("AutoExpFile")
    auto_line = prog.file_lines[auto_idx]
    instr_hdr_line = prog.file_lines[prog.instructions_index]

    assert f"(InsIdx {prog.instructions_count})" in auto_line
    assert f"Instructions {prog.instructions_count}" in instr_hdr_line


def test_smartprofile_parsing(mv_smart_profile_path):
    prog = MicroVuProgram(mv_smart_profile_path)
    assert prog.is_smartprofile is True
    assert prog.export_filepath == r"C:\TEXT\OUTPUT.txt"
    assert prog.instructions_index == 3
    assert prog.is_file_salted is True
    assert prog.instructions_count == 63
    assert prog.has_rotary is False
    assert prog.has_eof_batch_call is False
    assert prog.sequence_count == 1
