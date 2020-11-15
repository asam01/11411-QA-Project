import spacy
from spacy import displacy
from collections import Counter
from bs4 import BeautifulSoup
import requests
import re
import neuralcoref

def convertPronoun2Noun(text):
    doc = nlp(text)
    newText = ""
    for sentence in doc.sents():
        toModify = str(sentence)
        clusters = doc._.coref_clusters
        for pairs in clusters:
            for token in pairs:
                if token.pos_ == "NOUN":
                    temp = token
            for token in pairs:
                if token.pos_ == "PRON":
                    toModify.replace(str(token), str(temp))
        newText += toModify
    return newText
