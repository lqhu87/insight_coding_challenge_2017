from functions_donors import *

# to name two output files.
fn_zip = r'medianvals_by_zip.txt'
fn_date = r'medianvals_by_date.txt'

# to initialize the input and output
fh_input = initialize_input()
fh_output_zip, fh_output_date = initialize_output(fn_zip,fn_date)

# to calculate the median values, and store them
analyze(fh_input, fh_output_zip, fh_output_date)

# to close the files, and clean results
fh_output_zip.close()
fh_output_date.close()