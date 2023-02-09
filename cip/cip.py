#internal
# from config import config as c
from config.config import Configuration as conf
from config.config import Config
from extract_function import ExtractInfo

#external
import PyPDF2
import docx
import nltk
import json

import pathlib
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

class DictResult:
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
        self.other: str =other

    
class Cip:
    def __init__(self, language: str = None) -> None:
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')
        
        self.language: str = language
        c: conf = conf()
        self.config: Config = c.get_config()
        pass


    
    def __return_text_pdf(self, filename):
        '''
        La funzione legge il file PDF e restituisce il testo di esso
        '''
        content: str = ''

        #leggo il file
        reader = PyPDF2.PdfReader(filename)
        #numero di pagine utile per scorrerle e fare l'append di ognuna 
        n_pages = len(reader.pages)

        for n in range(n_pages):
            content += reader.pages[n].extract_text()
        
        #restituisce tutto il contenuo del pdf
        return content.lower()
    
    def __return_text_docx(self, filename):
        '''
        La funzione legge il file DOCX e restituisce il testo di esso
        '''
        full_text = []

        doc = docx.Document(filename)

        for para in doc.paragraphs:
            full_text.append(para.text)
        
        return ' '.join(full_text).lower()

    def read_file(self, filename):
        extension = pathlib.Path(filename).suffix
        text: str = ''

        if extension == '.pdf':
            text = self.__return_text_pdf(filename)
        elif extension == '.docx':
            text = self.__return_text_docx(filename)
       
        extract = ExtractInfo(self.config, text)

        dict_res: DictResult = DictResult(
            name = extract.name(),
            date_of_birth = extract.date_of_birth(),
            location = extract.location(),
            email = extract.email(),
            phone = extract.phonenumber(),
            programming_language = extract.return_info(self.config.prog_lang),
            soft_skill = extract.return_info(self.config.soft_skills),
            role = extract.return_info(self.config.role),
            other = extract.return_info(self.config.other),
            university = extract.university(),
        )

        result = self.__dict_result_builder(dict_res)        
        
        
        res_json = json.dumps(result, indent=4)
        return res_json
    
    def __dict_result_builder(self, dict: DictResult):


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




if __name__ == '__main__':
    r = Cip("it")
    
    test = r.read_file('Cerrone_Roberto_CV.docx')
    print('{\n"test":',test,' \n}')
    