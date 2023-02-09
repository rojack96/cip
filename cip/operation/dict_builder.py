

class DictOutput:
    def __init__(self, name: str, date_of_birth: str,location: str, email: str,phone: str, \
        university: str,programming_language: str,soft_skill: str,role: str,other: str) -> None:

        self.name: str = name
        self.date_of_birth: str = date_of_birth
        self.location: str = location
        self.email: str = email
        self.phone: str = phone
        self.university: str = university
        self.programming_language: str = programming_language
        self.soft_skill: str = soft_skill
        self.role: str = role
        self.other: str = other


class DictBuilder:
    def __init__(self, language: str) -> None:
        self.language:str = language

    def dict_result_builder(self, dict: DictOutput):


        result = {
            "name": dict.name,
            "date_of_birth": dict.date_of_birth,
            "location": dict.location,
            "email": dict.email,
            "phone": dict.phone,
            "university": dict.university,
            "programming_language": dict.programming_language,
            "soft_skill": dict.soft_skill,
            "role": dict.role,
            "other": dict.other,
            #"total_exp": total_exp,
        }

        result = self.__change_lang_keys(result, self.language)

        return result
    
    def __change_lang_keys(self,dictionary:dict, lang: str = None):
        if lang is None or lang != "it":
            return dictionary
        else:
            it_dict:dict = {}
            
            replace_key: dict = {
                "name": "nome",
                "date_of_birth": "data_di_nascita",
                "location": "residenza",
                "email": "email",
                "phone": "telefono",
                "university": "universita",
                "programming_language": "linguaggi_di_programmazione",
                "soft_skill": "soft_skill",
                "role": "ruolo",
                "other": "altro",
                #"total_exp": total_exp,
            }

            
            for old_key in dictionary.keys():
                new_key:str = replace_key[old_key]
                it_dict[new_key] = dictionary[old_key]

            return it_dict