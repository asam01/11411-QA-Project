import spacy
from spacy import displacy
from collections import Counter
from bs4 import BeautifulSoup
import requests
import re
import neuralcoref

def url_to_string(url):
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html5lib')
    for script in soup(["script", "style", 'aside']):
        script.extract()
    return " ".join(re.split(r'[\n\t]+', soup.get_text()))
# ny_bb = url_to_string('https://www.nytimes.com/2018/08/13/us/politics/peter-strzok-fired-fbi.html?hp&action=click&pgtype=Homepage&clickSource=story-heading&module=first-column-region&region=top-news&WT.nav=top-news')
# article = nlp(ny_bb)

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
