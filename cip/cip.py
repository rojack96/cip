#internal
# from config import config as c
from config.config import Configuration as conf
from config.config import Config
from extract_function import ExtractInfo

#external
import PyPDF2

import nltk
import json

from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree


class Cip:
    def __init__(self) -> None:
        c: conf = conf()
        self.config: Config = c.get_config()
        pass

    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')

    
    def __return_text_pdf(self, file):
        '''
        La funzione legge il file PDF e restituisce il testo di esso
        '''
        content: str = ''

        #leggo il file
        reader = PyPDF2.PdfReader(file)
        #numero di pagine utile per scorrerle e fare l'append di ognuna 
        n_pages = len(reader.pages)

        for n in range(n_pages):
            content += reader.pages[n].extract_text()
        
        #restituisce tutto il contenuo del pdf
        return content.lower()

    def read_file_pdf(self, filename):
        text: str = self.__return_text_pdf(filename)
       
        extract = ExtractInfo(self.config, text)

        name = extract.name()
        date_of_birth = extract.date_of_birth()
        location = extract.location()
        email = extract.email()
        phone = extract.phonenumber()
        programming_language = extract.return_info(self.config.prog_lang)
        soft_skill = extract.return_info(self.config.soft_skills)
        role = extract.return_info(self.config.role)
        other = extract.return_info(self.config.other)
        university = extract.university()

        result = {
            "name": name,
            "date_of_birth": date_of_birth,
            "location": location,
            "email": email,
            "phone": phone,
            "programming_language": programming_language,
            "soft_skill": soft_skill,
            "role": role,
            "other": other,
            #"total_exp": total_exp,
            "university": university,
        }
        
        res_json = json.dumps(result, indent=4)
        return res_json

if __name__ == '__main__':
    r = Cip()
    
    test = r.read_file_pdf('CV_RobertoCerrone.pdf')
    print('{\n"test":',test,' \n}')
    