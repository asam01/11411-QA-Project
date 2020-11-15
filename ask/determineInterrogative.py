import spacy
from spacy import displacy
from spacy.pipeline import EntityRecognizer
from collections import Counter
import requests
import re
nlp = spacy.load("en_core_web_sm")

import warnings
warnings.filterwarnings("ignore")

# who, what, where, when
def sentenceNER(sentence):  
    doc = nlp(sentence)
    entity_dict = {} 
    for ent in doc.ents: 
        entity_dict[ent] = ent.label_

    for word in entity_dict:
        tag = entity_dict[word]

        if tag == 'PERSON':
            entity_dict[word] = 'Who'

        elif tag == 'DATE' or tag == "TIME":
            entity_dict[word] = 'When'

        elif tag == "MONEY":
            entity_dict[word] = "How much"
        
        elif tag == 'LOC' or tag == 'GPE': 
            entity_dict[word] = "Where" 
        
        else:
            entity_dict[word] = "What"
            
    return entity_dict   

'''print(sentenceNER('Did Alan turing live in England?'))
print(sentenceNER('Is Carnegie Mellon in Pittsburgh, Pennsylvania?'))
print(sentenceNER('Is Alan Turing the father of computer science?'))'''