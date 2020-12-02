# uncomment to suppress warnings about version
import warnings
warnings.filterwarnings("ignore")

import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

import nltk
from nltk.corpus import wordnet as wn
import spacy
import benepar
from benepar.spacy_plugin import BeneparComponent

benepar.download('benepar_en2', quiet=True)
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe(BeneparComponent('benepar_en2'))
question_words = ["who", "where", "which", "when", "what", 'how many', 'why']

# NOTE need to handle how many and why questions

def findInterrogative(question):
    question = question.lower()
    words = question.split()
    for qWord in question_words:
        if qWord in question:
            return qWord

def answerWh(question, sentence):
    # We loop through each sentence and get the key word according to the interrogative
    interrogative = findInterrogative(question)
    answers = []

    entity_dict = {}
    sent = nlp(sentence)
    qsent = nlp(question) 
    for ent in sent.ents: 
        entity_dict[ent] = ent.label_

    if interrogative.lower() == "what":
        what_dep = ""
        for token in qsent: 
            if(token.text=="what"): 
                what_dep = token.dep_ 
        for token in sent:
            if (what_dep == token.dep_):
                if(token.text not in question):
                    answers += [token.text]

    for word in entity_dict:
        tag = entity_dict[word]
        
        if (tag == 'PERSON' or tag == 'ORG' or tag == 'NORP') and interrogative.lower() == "who":
            answers += [word]

        elif (tag == 'DATE' or tag == "TIME") and interrogative.lower() == "when":
            answers += [word]

        elif tag == "MONEY" and interrogative.lower() == "how much" :
            answers += [word]
        
        elif (tag == 'LOC' or tag == 'GPE') and interrogative.lower() == "where": 
            answers += [word]

    return answers


'''q1 =  "The what suggested that the goal 'might become the most famous goal in Fulham's history'?"

s1 = "The Guardian suggested that the goal 'might become the most famous goal in Fulham's history'."

q2 = "The Guardian suggested that the goal 'might become the most famous goal in what's history'?" 
print(answerWh(q2,s1))'''