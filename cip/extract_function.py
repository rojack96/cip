#internal
from config.config import Config

#external
import re
import phonenumbers
import spacy
import pandas as pd
import json
from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta     

class ExtractInfo:
    
    def __init__(self, config:Config, text:str):
        self.config:Config = config
        self.text: str = text

        self.italian_nlp = spacy.load('it_core_news_md')
        self.eng_nlp = spacy.load('en_core_web_trf')
        pass
    
    def return_info(self, context:str) -> list[str]:
        result = []

        try:
            for ctx in context:
                index = self.text.find(ctx)
                if index != -1:
                    result.append(ctx.title())
        except Exception as e:
            print(f"Exception as {e}")
        
        return result if result else None
    
    def name(self) -> str:
        '''
            Return name and surname
        '''
        spacy_parser = self.italian_nlp(self.text)

        """
        Testing
        
        for entity in spacy_parser.ents:
            if entity.label_ == 'PER':
                print("label", entity.label_, "text", entity.text)
        """
        try:
            for entity in spacy_parser.ents:
                if entity.label_ == 'PER':
                    #print("label", entity.label_, "text", entity.text)
                    name = entity.text
                    break
        except Exception as e:
            print(f"Exception as {e}")

        return name.title()
    
    def date_of_birth(self) -> str:
        '''
            Return a date of birth
        '''
        spacy_parser = self.eng_nlp(self.text)
        dates = []

        try:
            for entity in spacy_parser.ents:
                if entity.label_ == "DATE":
                    try:
                        date = parser.parse(str(entity.text), fuzzy=True)
                        dates.append(date)
                    except:
                        pass
            if dates:
                oldest: datetime = min(dates)
                age = relativedelta(datetime.now(), oldest).years
                oldest = oldest.strftime("%d/%m/%Y")
                
                if age >= 18:
                    return f"{oldest} ({age})"
            else:
                return None
        except Exception as e:
            print(f"Exception as {e}")
    
    def email(self) -> str:
        '''
            Return a email
        '''
        email: str = re.findall(r"([^@|\s]+@[^@]+\.[^@|\s]+)", self.text)
        if email:
            try:
                return email[0].split()[0].strip(';')
            except IndexError:
                return None
    
    def phonenumber(self) -> str:
        '''
            Return a phone number
        '''
        try:
            return list(iter(phonenumbers.PhoneNumberMatcher(self.text, None)))[0].raw_string
        except:
            try:
                return re.search(
                    r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})',
                    self.text).group()
            except:
                return ""
    
    def location(self):
        '''
            #TO IMPROVE#

            Ritorna due delle località con più occorrenze
        '''
        spacy_parser = self.italian_nlp(self.text)
        locations = []
        try:
            for entity in spacy_parser.ents:
                if entity.label_ == 'LOC':
                    locations.append(entity.text.title())
            
            loc = {'location':locations}
            df:pd.DataFrame = pd.DataFrame(loc, columns= ['location'])

            dups_loc = df.pivot_table(columns=['location'], aggfunc='size')
            
            dups_loc = dups_loc.nlargest(2).to_json(orient="split")
            dups_loc = json.loads(dups_loc)['index']
        except Exception as e:
            print(f"Exception as {e}")

        return dups_loc

    def university(self) -> bool:
        '''
            #TO IMPROVE#

            If university is a word present in CV return True, False otherwise

            The ideal would be return an array of university
        '''
        uni = self.text.find("università")
        try:
            if uni == -1:
                return False    
            return True
        except Exception as e:
            print(f"Exception as {e}")
            

