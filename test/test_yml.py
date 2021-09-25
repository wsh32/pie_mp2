import yaml
from yaml import Loader


with open("test_msg.yml", "r") as ymlfile:
    data = yaml.load(ymlfile, Loader=Loader)

print(data)

for d in data:
    print(data[d])
