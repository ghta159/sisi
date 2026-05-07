#!/usr/bin/env python3
import json
from difflib import SequenceMatcher

print("paste json")
json_input = []

while True:
    line = input()
    if line.strip() == "":
        break
    json_input.append(line)

json_data = json.loads("\n".join(json_input))

print("paste liste")
image_version = {}

while True:
    line = input()
    if line.strip() == "":
        break
    l = line.split()
    image_version[l[0]] = l[1]
#print(image_version)

foo = {}
for i in image_version:
    s = i.replace("-", " ").casefold()
    max_so_far = float("-inf")
    foo[i]={"check_version": image_version[i],
            "qa_service": "",
            "qa_version": "",
            }
    for j in json_data:
        k = j.replace("-", " ").casefold()
        score = SequenceMatcher(None, s, k).ratio()
        #if score > 0.6:
        if score > 0.74:
            if score > max_so_far:
                max_so_far = score
                foo[i]={"check_version": image_version[i],
                        "qa_service": j,
                        "qa_version": json_data[j]
                        }

def parse_version(v):
    return tuple(map(int, (v or "0.0.0.0").split(".")))

GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

a,b,c,d = "prod image", "version", "qa image", "version"
print(f"{a:<40} {b:<32} {c:<32} {d}")

for i in foo:
    prod_service = i
    prod_version = foo[i]['check_version']
    qa_service = foo[i]['qa_service']
    qa_version = foo[i]['qa_version']
    check = ""
    if qa_service =="":
        prod_service = BLUE+prod_service+RESET
    else:
        if parse_version(qa_version) >= parse_version(prod_version):
            prod_service = GREEN+prod_service+RESET
            prod_version = GREEN+prod_version+RESET
            check = "v"
        else:
            prod_service = RED+prod_service+RESET
            prod_version = RED+prod_version+RESET           

    print(f"{prod_service:<40} {prod_version:<32} {qa_service:<32} {qa_version} {check}")


