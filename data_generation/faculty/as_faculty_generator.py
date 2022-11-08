from utils import *

def generate_as_faculty_data(drexel_json):
    as_professors = []
    professor_html = html("https://drexel.edu/coas/faculty-research/faculty-directory/")

    for element in professor_html.find_all("div", class_="fname"):
        professor_name = regex.sub(r"\s+", " ", element.find("h3").find("a").decode_contents().strip())
        print(f"Getting data for Professor {professor_name}")
        professor_role = list(map(lambda x: x.strip(), regex.sub(r"\n+", "\n", element.parent.get_text().strip().replace("\r", "")).split("\n")[1].strip().split(";")))
        professor_email = find(lambda elem: elem["href"].startswith("mailto:"), element.parent.find_all("a")).decode_contents().strip()
        professor_department = element.parent.parent.parent.find_all("td")[1].find("li").decode_contents().strip()
        professor_department = professor_department if professor_department else "unknown"
        professor_email = professor_email if professor_email else "unknown"
        professor_interests = element.parent.parent.parent.find_all("td")[2].find("p")
        professor_interests = professor_interests.decode_contents().strip() if professor_interests else "unknown"
        as_professors.append({
            "name": professor_name,
            "titles": professor_role,
            "email": professor_email,
            "interests": professor_interests
        })

    find(lambda college: college["name"] == "College of Arts and Sciences", drexel_json["colleges"])["faculty"] = as_professors