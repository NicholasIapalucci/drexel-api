from utils import *
from faculty_generator import *
from course_generator import *
from organization_generator import *

drexel_json = { "colleges": [] }
generate_course_data(drexel_json)
generate_organization_data(drexel_json)
generate_faculty_data(drexel_json)

open("src/data/drexel.json", "w").write(regex.sub(r"\\u\d+", "'", json.dumps(drexel_json, indent=4)))
