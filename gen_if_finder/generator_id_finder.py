import requests
import json
#https://www.namegeneratorfun.com/api/namegenerator?generatorType=list&firstName=&lastName=&minLength=0&maxLength=255&sexId=1&generatorId=35
main_url = "https://www.namegeneratorfun.com/api/namegenerator?generatorType=list&firstName=&lastName=&minLength=0&maxLength=255&sexId=1&generatorId=1"

dict_gen_ids = {}
for num in range(0, 500):
    custom_url = main_url[:137] + str(num)
    response = requests.get(custom_url)
    if response.status_code != 200:
        continue
    json_response = json.loads(response.text)

    dict_gen_ids[f"{json_response['generator']}"] = json_response["generatorId"]

with open("generator_ids.json", "w") as json_file:
    json.dump(dict_gen_ids, json_file, sort_keys=True)


