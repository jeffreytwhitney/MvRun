import os

import pytest

from lib.MicroVuFileProcessor import get_processor, ProcessorException
from lib.Utilities import get_utf_encoded_file_lines


def test_properties_setters_getters(mv_prompt_for_export_path, output_dir):
    mv_file_name = os.path.basename(mv_prompt_for_export_path)
    output_file_name = str(os.path.join(output_dir, mv_file_name))
    processor = get_processor(mv_prompt_for_export_path, False, '123456', '4404', '1234', [1], output_file_name)
    assert processor is not None
    assert processor.employee_id == "4404"
    assert processor.job_number == "1234"
    assert processor.machine_number == "123456"
    assert processor.is_setup is False


def test_process_file_creates_output_file_prompt_case(mv_prompt_for_export_path, output_dir):
    mv_file_name = os.path.basename(mv_prompt_for_export_path)
    output_file_name = str(os.path.join(output_dir, mv_file_name))
    processor = get_processor(mv_prompt_for_export_path, False, '123456', '4404', '1234', [1], output_file_name)
    processor.process_file()
    assert os.path.exists(output_file_name), f"Expected output file to exist: {output_file_name}"
    file_lines = get_utf_encoded_file_lines(output_file_name)
    assert len(file_lines) > 0
    title_line = file_lines[2]
    assert "(AutoConf 0)" in title_line
    assert "(AutoExpFile \"M:\\2030-6516-1300_OP10_REVB_.csv\")" in title_line
    assert "(Name \"EMPLOYEE\") (ExpLab) (ExpProps Txt) (Txt \"4404\")" in file_lines[16]
    assert "(Name \"JOB\") (ExpLab) (ExpProps Txt) (Txt \"1234\")" in file_lines[17]
    assert "(Name \"MACHINE\") (ExpLab) (ExpProps Txt) (Txt \"123456\")" in file_lines[18]
    assert "(Name \"SEQUENCE\") (ExpLab) (ExpProps Txt) (Txt \"1\")" in file_lines[20]
    assert "(Name \"CallEOFBatch\")" in file_lines[673]


def test_process_file_creates_output_file_smartprofile(mv_smart_profile_path, output_dir):
    mv_file_name = os.path.basename(mv_smart_profile_path)
    output_file_name = str(os.path.join(output_dir, mv_file_name))
    processor = get_processor(mv_smart_profile_path, False, '123456', '4404', '1234', [1], output_file_name)
    processor.process_file()
    assert os.path.exists(output_file_name)
    file_lines = get_utf_encoded_file_lines(output_file_name)
    assert len(file_lines) > 0
    title_line = file_lines[2]
    assert "(AutoConf 0)" in title_line
    assert "OUTPUT.txt" in title_line
    assert "(Name \"EMPLOYEE\") (ExpLab) (ExpProps Txt) (Txt \"4404\")" in file_lines[17]
    assert "(Name \"JOB\") (ExpLab) (ExpProps Txt) (Txt \"1234\")" in file_lines[18]
    assert "(Name \"MACHINE\") (ExpLab) (ExpProps Txt) (Txt \"123456\")" in file_lines[19]
    assert "(Name \"SEQUENCE\") (ExpLab) (ExpProps Txt) (Txt \"1\")" in file_lines[21]
    assert "(Name \"CallEOFBatch\")" in file_lines[331]


def test_process_file_does_not_raise(mv_multipart_path, output_dir):
    mv_file_name = os.path.basename(mv_multipart_path)
    output_file_name = str(os.path.join(output_dir, mv_file_name))
    processor = get_processor(mv_multipart_path, False, '123456', '4404', '1234', [1, 2, 3, 4, 5], output_file_name)
    processor.process_file()
    assert os.path.exists(output_file_name)
    file_lines = get_utf_encoded_file_lines(output_file_name)
    assert len(file_lines) > 0
    title_line = file_lines[2]
    assert "(AutoConf 0)" in title_line
    assert "(AutoExpFile \"M:\\110017557-B_OP10_SIDE VIEW_REVE_.csv\")" in title_line
    assert "(Name \"EMPLOYEE\") (ExpLab) (ExpProps Txt) (Txt \"4404\")" in file_lines[16]
    assert "(Name \"JOB\") (ExpLab) (ExpProps Txt) (Txt \"1234\")" in file_lines[17]
    assert "(Name \"MACHINE\") (ExpLab) (ExpProps Txt) (Txt \"123456\")" in file_lines[18]
    assert "(Name \"SEQUENCE1\") (ExpLab) (ExpProps Txt) (Txt \"1\")" in file_lines[20]
    assert "(Name \"SEQUENCE2\") (ExpLab) (ExpProps Txt) (Txt \"2\")" in file_lines[21]
    assert "(Name \"SEQUENCE3\") (ExpLab) (ExpProps Txt) (Txt \"3\")" in file_lines[22]
    assert "(Name \"SEQUENCE4\") (ExpLab) (ExpProps Txt) (Txt \"4\")" in file_lines[23]
    assert "(Name \"SEQUENCE5\") (ExpLab) (ExpProps Txt) (Txt \"5\")" in file_lines[24]
    assert "(Name \"CallEOFBatch\")" in file_lines[1745]


def test_process_multipart_file(mv_multipart_path, output_dir):
    mv_file_name = os.path.basename(mv_multipart_path)
    output_file_name = str(os.path.join(output_dir, mv_file_name))
    with pytest.raises(ProcessorException):
        processor = get_processor(mv_multipart_path, False, '123456', '4404', '1234', [1, 2, 3, 4], output_file_name)
        processor.process_file()
