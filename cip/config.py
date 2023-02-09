from collections import namedtuple

import json

class Config:
    prog_lang: str
    soft_skills: str
    other: str
    role:str

def configDecoder(configDict):
    return namedtuple('X', configDict.keys())(*configDict.values())


f = open('config.json', "r")
file = f.read()
f.close()

config: Config = json.loads(file, object_hook=configDecoder)