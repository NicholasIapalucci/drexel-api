from bs4 import BeautifulSoup
import json
from urllib.request import urlopen
import re as regex

drexel_json = { "colleges": [] }

def find(pred, iterable):
  for element in iterable:
      if pred(element):
          return element
  return None

def html(url):
    return BeautifulSoup(urlopen(url).read(), features = "html.parser")

def parse_prereqs(prereq_string):
    prereq_string = regex.sub(r"([A-Z])\s(\d+)", r"\1-\2", prereq_string)

    # Tokenize
    token_types = {
        "class": r"^[A-Z]+\-\d+",
        "whitespace": r"^\s+",
        "grade": r"^\[Min Grade: (.+?)\]",
        "and": r"^and\b",
        "or": r"^or\b",
        "left parentheses": r"^\(",
        "right parentheses": r"^\)"
    }
    tokens = []
    remaining_string = prereq_string
    while(remaining_string):
        match_found = False
        for type_, regexp in token_types.items():
            match = regex.match(regexp, remaining_string)
            if match:
                if type_ == "grade": tokens.append({ "type": type_, "value": match.group(1) })
                elif type_ != "whitespace": tokens.append({ "type": type_, "value": match.group(0) })
                remaining_string = remaining_string[len(match.group(0)):]
                match_found = True
                break
        if not match_found: return [remaining_string]

    # Parser

    def next(type_):
        if len(tokens_to_parse) == 0: return False
        if type_ and tokens_to_parse[0]["type"] != type_: raise Exception("Expected type " + type_ + " but found " + tokens_to_parse[0]['type'] + " in\n" + "\n".join(map(lambda token : str(token), tokens)))
        return tokens_to_parse.pop(0)

    def next_is(type_):
        return tokens_to_parse[0]["type"] == type_ if len(tokens_to_parse) > 0 else False

    def parse_and_or(left):
        while next_is("and"):
            next("and")
            expr = parse_expr()
            if type(expr) is list and type(left) is list: left = [*left, *expr]
            elif type(expr) is list: left = [left, *expr]
            elif type(left) is list: left = [*left, expr]
            else: left = [left, expr]
        while next_is("or"):
            next("or")
            expr = parse_expr()
            if "one of" in expr: left = { "one of": [left, *expr.get("one of")] }
            else: left = { "one of": [left, expr] }
        return left

    def parse_expr():
        if next_is("left parentheses"):
            next("left parentheses")
            expr = parse_expr()
            next("right parentheses")
            if (next_is("and") or next_is("or")): return parse_and_or(expr)
            return expr
        if next_is("class"):
            course_name = next("class")["value"]
            grade = "Any"
            if next_is("grade"): grade = next("grade")["value"]
            return parse_and_or({
                "codeName": course_name,
                "minimum grade": grade
            })
        raise Exception("Unexpected token: " + str(tokens_to_parse[0]))

    prerequisites = []
    tokens_to_parse = tokens.copy()

    while next_is("or") or next_is("and"):
        next(None)

    while(tokens_to_parse):
        prerequisites.append(parse_expr())

    if len(prerequisites) == 1 and type(prerequisites[0]) is list: return prerequisites[0]
    return prerequisites

ugSoup = html("https://catalog.drexel.edu/coursedescriptions/quarter/undergrad")
for element in ugSoup.find_all("a"):
    text_contents = element.decode_contents()
    if "(" in text_contents and ")" in text_contents:
        href = element.get("href")
        major_soup = html("https://catalog.drexel.edu" + href)
        major_name = text_contents[:text_contents.index("(") - 1].replace("&amp;", "&")
        print("Getting stats for " + major_name)

        for course_block in major_soup.find_all("div", class_="courseblock"):
            
            # Proper name + Code name
            title = course_block.find_all("span", class_="cdspacing")

            # Code name
            code = regex.sub(r"[^\w]", "-", title[0].decode_contents()[:-2])

            # Proper name
            name = title[1].decode_contents().replace("&amp;", "&")

            # Credits
            credits = title[2].previous_sibling.strip()
            if "-" in credits: credits = credits[credits.index("-") + 1:].strip()
            credits = int(float(credits))

            # Prequisites
            prereqs = course_block.find_all("b")[-1]
            prereq_list = []
            if prereqs and not "credit" in prereqs.next_sibling: prereq_list = parse_prereqs(prereqs.next_sibling.strip())

            # College 
            college = course_block.find("b").next_sibling.strip()

            # Get college object
            college_object = find(lambda x: x.get("name") == college, drexel_json["colleges"])
            if not college_object:
                college_object = { "name": college, "majors": [] }
                drexel_json["colleges"].append(college_object)

            # Get major object
            major_object = find(lambda major: major["name"] == major_name, college_object["majors"])
            if not major_object:
                major_object = { "name": major_name, "courses": [] }
                college_object["majors"].append(major_object)

            # Get class Object
            class_object = {
                "codeName": code,
                "properName": name,
                "credits": credits,
                "majorName": major_name,
                "prerequisites": prereq_list if prereq_list else []
            }
            major_object["courses"].append(class_object)

# Clubs

clubs_html = BeautifulSoup(open("data_generation/pages/clubs.html").read(), features = "html.parser")
clubs = clubs_html.find_all("div", class_="MuiPaper-root MuiCard-root MuiPaper-elevation3 MuiPaper-rounded")

organizations = []

for club_element in clubs:
    club_div = club_element.find("div").find("span").find("div").find("div")
    club_name = regex.sub(r"\s+", " ", club_div.find("div", attrs={"alt": None}).decode_contents()).strip()
    club_desc = regex.sub(r"\s+", " ", club_div.find("p").decode_contents()).strip()
    link = club_element.parent["href"]

    organizations.append({
        "name": club_name,
        "description": club_desc
    })

drexel_json["studentOrganizations"] = organizations

open("src/data/drexel.json", "w").write(json.dumps(drexel_json, indent=4))
