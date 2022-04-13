import random
import requests
import json

url_global = 'https://www.namegeneratorfun.com/api/namegenerator?generatorType=list&firstName=&lastName=&minLength=0&maxLength=255&sexId=1&generatorId=43'

# https://www.namegeneratorfun.com/api/namegenerator?generatorType=list&firstName=&lastName=&minLength=0&maxLength=255&sexId=2&generatorId=43

dict_from_json_male = 0
dict_from_json_female = 0
dict_types_of_gen = {"Korea": "43", "China": "35", "World": "159"}
dict_sex = {"Male": "1", "Female": "2"}

type_of_gen = "Korea"

file_email_domains = open(f"email_domains/{type_of_gen}_email_domains.txt", "r", encoding="utf-8")
file_names = open(f"{type_of_gen}_names.txt", "w", encoding="utf-8")
file_emails = open(f"{type_of_gen}_emails.txt", "w", encoding="utf-8")

email_domains_list = [email.rstrip("\n") for email in file_email_domains.readlines()]


def custom_url(sex, country, url):
    return url[:123] + dict_sex[sex] + url[124:137] + dict_types_of_gen[country]


def name_to_email(name_given):
    def fullname_with_third_name_to_email(name_with_third_name):
        email = random.choice(["", str(random.randint(0, 99)), str(random.randint(1950, 2022)), "", "", "", "", ""]) + \
                name_with_third_name[
                    0] + random.choice(
            ["", ".", ".", "", "", "", str(random.randint(0, 9)), "", "."]) + name_with_third_name[
                    1] + random.choice(
            ["", ".", "", "."]) + name_with_third_name[2] + random.choice(
            [str(random.randint(1950, 2020)), str(random.randint(0, 999)), "", "", ""]) + "@" + random.choice(
            email_domains_list)
        return email

    def fullname_without_third_name_to_email(name_without_third_name):
        email = random.choice(["", str(random.randint(0, 99)), str(random.randint(1950, 2022)), "", "", "", "", ""]) + \
                name_without_third_name[
                    0] + random.choice(
            ["", ".", ".", "", "", ".", ".", str(random.randint(0, 9)), "", "."]) + name_without_third_name[
                    1] + random.choice(
            ["", ".", "", "", str(random.randint(
                0, 99)),
             str(random.randint(
                 0,
                 9))]) + "@" + random.choice(
            email_domains_list)
        return email

    list_parts_of_fullname = name_given.lower().replace("-", " ").split()

    if len(list_parts_of_fullname) == 3:
        return fullname_with_third_name_to_email(list_parts_of_fullname)
    elif len(list_parts_of_fullname) == 2:
        return fullname_without_third_name_to_email(list_parts_of_fullname)


for _ in range(500):
    json_response_male = requests.get(custom_url("Male", type_of_gen, url_global)).text
    json_response_female = requests.get(custom_url("Female", type_of_gen, url_global)).text

    try:
        dict_from_json_male = json.loads(json_response_male)
        dict_from_json_female = json.loads(json_response_female)
    except:
        pass

    for name in dict_from_json_male["names"]:
        file_names.write(f"{name}\r\n")
        file_emails.write(f"{name_to_email(name)}\r\n")

    for name in dict_from_json_female["names"]:
        file_names.write(f"{name}\r\n")
        file_emails.write(f"{name_to_email(name)}\r\n")
