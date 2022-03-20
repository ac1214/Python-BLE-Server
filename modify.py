import json
import random
import time

while(True):
    time.sleep(2)

    data = {}
    with open('config.json', "r") as json_file:
        data = json.load(json_file)
    
    data["battery-precent"] -= random.randint(5,10)
    if data["battery-precent"] <= 0:
        data["battery-precent"] = 100

    with open('config.json', "w") as json_file:
        json.dump(data, json_file)
