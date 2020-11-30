# uncomment to suppress warnings about version
import warnings
warnings.filterwarnings("ignore")

import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

import nltk
import spacy
import benepar
from benepar.spacy_plugin import BeneparComponent

benepar.download('benepar_en2', quiet=True)
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe(BeneparComponent('benepar_en2'))


# Input: the question statement, and top 3 relevant sentences we identified 
# using the function find_sentence(question, corpus);
# Output: a list of 3 potential answers, which are in the form of the short phrase. 
def answerWh(question, sentences):
    # We loop through each sentence and get the key word according to the interrogative
    interrogative = question.split(" ")[0]
    answers = []

    for sentence in sentences:
        entity_dict = {}
        sent = nlp(sentence)
        for ent in sent.ents: 
            entity_dict[ent] = ent.label_

        if interrogative.lower() == "what":
            for token in sent:
                if 'obj' in token.dep_:
                    answers += [token.text]

        for word in entity_dict:
            tag = entity_dict[word]
            
            if tag == 'PERSON' and interrogative.lower() == "who":
                answers += [word]

            elif (tag == 'DATE' or tag == "TIME") and interrogative.lower() == "when":
                answers += [word]

            elif tag == "MONEY" and interrogative.lower() == "how much" :
                answers += [word]
            
            elif (tag == 'LOC' or tag == 'GPE') and interrogative.lower() == "where": 
                answers += [word]

    return answers