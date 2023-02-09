#internal
# from config import config as c
from config.config import Configuration as conf
from config.config import Config
from operation.extract_function import ExtractInfo
from operation.dict_builder import DictOutput, DictBuilder

#external
import PyPDF2
import docx
import nltk
import json

import pathlib
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

    
class Cip:
    def __init__(self, language: str = None) -> None:
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')
        
        self.dict_builder = DictBuilder(language)
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

        dict_res: DictOutput = DictOutput(
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

        result = self.dict_builder.dict_result_builder(dict_res)        
        
        
        res_json = json.dumps(result, indent=4)
        return res_json

if __name__ == '__main__':
    r = Cip("it")
    
    test = r.read_file('Cerrone_Roberto_CV.docx')
    print('{\n"test":',test,' \n}')
    