from lib import MicroVuFileProcessor

input_filepath = "C:\\TEST\\MVRun\\input\\446007 DATUM F UP.iwp"
output_filepath = "C:\\TEST\\MVRun\\output\\446007 DATUM F UP.iwp"
machine_name = "P2001-50"
employee_id = "4404"
job_number = "123456789"
sequence_number = "1"

processor = MicroVuFileProcessor.get_processor(input_filepath, output_filepath, machine_name, employee_id
                                               , job_number, sequence_number)

processor.process_file()