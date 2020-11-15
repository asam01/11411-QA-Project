import spacy
from spacy import displacy
from collections import Counter
from bs4 import BeautifulSoup
import requests
import re
import neuralcoref

nlp = spacy.load('en_core_web_lg')
neuralcoref.add_to_pipe(nlp)

def convertPronoun2Noun(text):
    print('beginning of function')
    doc = nlp(text)
    print('after doc = nlp')
    newText = ""
    print('in function')
    for sentence in doc.sents:
        toModify = str(sentence)
        clusters = doc._.coref_clusters
        for pairs in clusters:
            for token in pairs:
                for t in token:
                    if t.pos_ == "NOUN" or t.pos_=="PROPN":
                        temp = token.text
            for token in pairs:
                for t in token:
                    if t.pos_ == "PRON":
                        toModify.replace(str(token), str(temp))
        newText += toModify

    print('before returning')
    return newText
