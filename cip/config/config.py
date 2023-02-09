from collections import namedtuple
import json

class Config:
        prog_lang: str
        soft_skills: str
        other: str
        role:str

class Configuration:
    def __init__(self) -> None:
        pass

    def __configDecoder(self,configDict: dict):
        return namedtuple('X', configDict.keys())(*configDict.values())

    def __read_config_file(self) -> str:
        try:
            f = open('./config/config.json', "r")
            file = f.read()
            f.close()
        except:
            print("File not found")
        
        return file
    
    def get_config(self):
        file: str = self.__read_config_file()
        config: Config = json.loads(file, object_hook=self.__configDecoder)
        return config