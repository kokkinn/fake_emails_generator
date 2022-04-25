import random
import requests
import json
from openpyxl import Workbook

url_global = 'https://www.namegeneratorfun.com/api/namegenerator?generatorType=list&firstName=&lastName=&minLength=0&maxLength=255&sexId=1&generatorId=43'

# https://www.namegeneratorfun.com/api/namegenerator?generatorType=list&firstName=&lastName=&minLength=0&maxLength=255&sexId=2&generatorId=43

dict_from_json_male = 0
dict_from_json_female = 0
dict_types_of_gen = {"Korea": "43", "China": "35", "USA": "159"}
dict_sex = {"Male": "1", "Female": "2"}

type_of_gen = "USA"

file_email_domains = open(f"email_domains/{type_of_gen}_email_domains.txt", "r", encoding="utf-8")
file_positions = open("positions.txt", "r", encoding="utf-8")

email_domains_list = [email.rstrip("\n") for email in file_email_domains.readlines()]
positions_list = [position.rstrip("\n") for position in file_positions.readlines()]


def custom_url(sex, country, url):
    return url[:123] + dict_sex[sex] + url[124:137] + dict_types_of_gen[country]


def name_to_email(length_of_name, list_parts_of_fullname, date_of_birth):
    def fullname_with_third_name_to_email(name_with_third_name):
        email = random.choice(["", str(random.randint(0, 99)), "", "", "", "", ""]) + \
                name_with_third_name[
                    0] + random.choice(
            ["", ".", ".", "", "", "", str(random.randint(0, 9)), "", "."]) + name_with_third_name[
                    1] + random.choice(
            ["", ".", "", "."]) + name_with_third_name[2] + random.choice(
            [str(date_of_birth), str(random.randint(0, 999)), "", "", ""]) + "@" + random.choice(
            email_domains_list)
        return email

    def fullname_without_third_name_to_email(name_without_third_name):
        email = random.choice(["", str(random.randint(0, 99)), str(date_of_birth), "", "", "", "", ""]) + \
                name_without_third_name[
                    0] + random.choice(
            ["", ".", ".", "", "", ".", ".", str(random.randint(0, 9)), "", "."]) + name_without_third_name[
                    1] + random.choice(
            ["", "", "", "", str(random.randint(
                0, 99)),
             str(random.randint(
                 0,
                 9))]) + "@" + random.choice(
            email_domains_list)
        return email

    if length_of_name == 2:
        return fullname_without_third_name_to_email(list_parts_of_fullname)
    elif length_of_name == 3:
        return fullname_with_third_name_to_email(list_parts_of_fullname)


def get_json_from_web(sex, gen_type):
    return requests.get(custom_url(sex, gen_type, url_global)).text


def create_personal_data(name, sex):
    personal_data = {}
    list_parts_of_fullname = name.replace("-", " ").split()
    len_of_fullname = len(list_parts_of_fullname)

    personal_data["Country"] = type_of_gen
    personal_data["Position"] = random.choice(positions_list)
    personal_data["Date_added"] = ""
    personal_data["Year_of_birth"] = random.randint(1950, 1995)
    personal_data["Age"] = 2022 - personal_data["Year_of_birth"]
    personal_data["Number"] = ""
    personal_data["Sex"] = sex

    if len_of_fullname == 2:
        personal_data["First_name"] = list_parts_of_fullname[0]
        personal_data["Last_name"] = list_parts_of_fullname[1]
        personal_data["Email"] = name_to_email(len_of_fullname, [name.lower() for name in list_parts_of_fullname],
                                               personal_data["Year_of_birth"])
    elif len_of_fullname == 3:
        list_parts_of_fullname_for_3 = name.split(" ")
        personal_data["First_name"] = list_parts_of_fullname_for_3[0]
        personal_data["Last_name"] = list_parts_of_fullname_for_3[1]
        personal_data["Email"] = name_to_email(len_of_fullname, [name.lower() for name in list_parts_of_fullname],
                                               personal_data["Year_of_birth"])

    return personal_data


def write_to_excel(data, sheet):
    sheet[f"A{counter_rows}"] = data["First_name"]
    sheet[f"B{counter_rows}"] = data["Last_name"]
    sheet[f"C{counter_rows}"] = data["Email"]
    sheet[f"D{counter_rows}"] = data["Country"]
    sheet[f"E{counter_rows}"] = data["Position"]
    sheet[f"F{counter_rows}"] = data["Date_added"]
    sheet[f"G{counter_rows}"] = data["Age"]
    sheet[f"H{counter_rows}"] = data["Year_of_birth"]
    sheet[f"I{counter_rows}"] = data["Number"]
    sheet[f"J{counter_rows}"] = data["Sex"]


workbook = Workbook()
sheet_danya_data = workbook.active
counter_cols = 0
counter_rows = 0

for _ in range(25):
    try:
        list_of_male_names = json.loads(get_json_from_web("Male", type_of_gen))["names"]
        list_of_female_names = json.loads(get_json_from_web("Female", type_of_gen))["names"]
    except:
        continue

    for name in list_of_male_names:
        counter_rows += 1
        dict_personal_data = create_personal_data(name, "Male")
        write_to_excel(dict_personal_data, sheet_danya_data)

    for name in list_of_female_names:
        counter_rows += 1
        dict_personal_data = create_personal_data(name, "Female")
        write_to_excel(dict_personal_data, sheet_danya_data)

workbook.save(filename="FOr_danya.xlsx")
