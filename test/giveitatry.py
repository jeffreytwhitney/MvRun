from lib import MicroVuFileProcessor

input_filepath = "C:\\TEST\\MVRun\\Input\\110017557-B REV E\\110017557-B SIDE VIEW MULTI.iwp"
output_filepath = "C:\\TEST\\MVRun\\output\\110017557-B SIDE VIEW MULTI.iwp"
machine_name = "P2001-50"
is_setup = False
employee_id = "4404"
job_number = "123456789"
sequence_numbers = [1, 2, 3, 4, 5]

processor = MicroVuFileProcessor.get_processor(input_filepath, output_filepath)
processor.process_file(is_setup, machine_name, employee_id, job_number, sequence_numbers)


