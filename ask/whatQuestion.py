import spacy
import benepar
from benepar.spacy_plugin import BeneparComponent
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe(BeneparComponent('benepar_en2'))
    
# uncomment to suppress warnings about version
import warnings
warnings.filterwarnings("ignore")

# use parse tree to determine which word to replace with interrogative

# assume inputs are results from compound binary questions
# and/or simple binary questions


# input: 'Did Alan Turing live in England?', {Alan Turing: Who, England: Where}
# or 'Is Alan Turing nice?' {Alan Turing: Who}
def generateQFromQ(question, entity_dict):
    questions_list = []
    doc = nlp(question)

    sent = list(doc.sents)[0]
    children = list(sent._.children)
    puncts = '?!.,;:-'
    constituents = list(sent._.constituents)
    stringtotakeout = ''
    questionword = '' 
    for clause in constituents:
        #print(clause.text, clause._.labels)
        if 'PP' in clause._.labels:
            for word in entity_dict: 
                if((entity_dict[word]=='When' or entity_dict[word]=='Where') and word in clause.text):
                    stringtotakeout = clause.text
                    questionword = entity_dict[word]

        #if 'NP' in clause._.labels: 
        #    for word in entity_dict: 
        #        if()
                 

    question = question.split(stringtotakeout) 
    question = questionword + ' ' + "".join(question)


    print(question)


                    

    


def generateQFromSentence(sentence, entity_dict):
    raise Exception('not implemented')


generateQFromQ('Did Alan Turing live in England?', {'Alan Turing': 'Who', 'England': 'Where'})
generateQFromQ('Was Alan Turing born in 1915?', {'Alan Turing': 'Who', '1915': 'When'})
generateQFromQ('Is Carnegie Mellon in Pittsburgh, Pennsylvania?', {'Carnegie Mellon': 'What', 'Pittsburgh': 'Where', 'Pennsylvania': 'Where'})
generateQFromQ('Is Alan Turing the father of computer science?', {'Alan Turing': 'Who'})