import spacy
import benepar
from benepar.spacy_plugin import BeneparComponent

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe(BeneparComponent('benepar_en2'))
    
# uncomment to suppress warnings about version
import warnings
warnings.filterwarnings("ignore")



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

        if interrogative == "What":
            for token in sent:
                if 'obj' in token.dep_:
                    answers += [token.text]

        for word in entity_dict:
            tag = entity_dict[word]
            
            if tag == 'PERSON' and interrogative == "Who":
                answers += [word]

            elif (tag == 'DATE' or tag == "TIME") and interrogative == "When":
                answers += [word]

            elif tag == "MONEY" and interrogative == "How much" :
                answers += [word]
            
            elif (tag == 'LOC' or tag == 'GPE') and interrogative == "Where": 
                answers += [word]

    return answers