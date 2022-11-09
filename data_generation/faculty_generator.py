from faculty.as_faculty_generator import *
from faculty.cci_faculty_generator import *
from faculty.westphal_faculty_generator import *

def generate_faculty_data(drexel_json):
    generate_as_faculty_data(drexel_json)
    generate_cci_faculty_data(drexel_json)
    generate_westphal_faculty_data(drexel_json)