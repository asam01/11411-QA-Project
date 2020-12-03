import warnings
warnings.filterwarnings("ignore")

import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

import spacy
import benepar
benepar.download('benepar_en2', quiet=True)

from benepar.spacy_plugin import BeneparComponent
from compoundBinary import preprocess
from determineInterrogative import sentenceNER
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe(BeneparComponent('benepar_en2'))


# use parse tree to determine which word to replace with interrogative

# assume inputs are results from compound binary questions
# and/or simple binary questions

def generateWhenWhereFromQ(question, entity_dict):
    doc = nlp(question)

    sent = list(doc.sents)[0]
    children = list(sent._.children)
    puncts = '?!.,;:-'
    constituents = list(sent._.constituents)
    stringtotakeout = ''
    questionword = '' 
    for clause in constituents:
        if 'PP' in clause._.labels:
            for word in entity_dict: 
                if((entity_dict[word]=='When' or entity_dict[word]=='Where') and word.text in clause.text):
                    stringtotakeout = clause.text
                    questionword = entity_dict[word]
                    
                    # prioritize when/where questions over who and what
                    all_words = question.split(" ")
                    question = all_words[0].lower() + " " + " ".join(all_words[1:])
                    question = question.split(stringtotakeout)
                    question = questionword + " " + "".join(question) 
                    return question 
          
def generateWhoFromSentence(sentence, properNoun):
    clauses = preprocess(sentence)
    questions = [] 
    for sent in clauses: 
        doc = nlp(sent)
        sent2 = list(doc.sents)[0]
        constituents = list(sent2._.constituents)
        stringtotakeout = ''
        questionword = '' 
        for clause in constituents:
            if 'NP' in clause._.labels:
                if(properNoun.text == clause.text): 
                    stringtotakeout = clause.text
                    questionword = "who"
                    question = sent.split(stringtotakeout)

                    # capitalize if the interrogative starts the question
                    if len(question[0]) == 0:
                        questionword = 'Who'
                    question = question[0] + questionword + question[1]
                    questions.append(question[:len(question)-1] + '?')
    
    return questions

def generateWhatFromSentence(sentence, properNoun):
    sentence = sentence[:(len(sentence)-1)] # remove exisiting punctuation
    question = sentence.split(properNoun.text)
    question = question[0] + 'what' + question[1] + '?'
    return question

# Alan Turing liked potatoes because they are delicious.
# --> Did Alan Turning like potatoes because they are delicious?
# --> Why did Alan Turing like potatoes?
def generateWhyFromQ(question):
    words_to_split_on = ['because', 'since', 'due to']
    for word in words_to_split_on: 
        if(word in question): 
            question = question.split(word) 
            question = 'Why' + question[0] + '?'
            return question 

def generateHowManyFromSentence(sentence, properNoun):
    sentence = sentence[:(len(sentence)-1)] # remove exisiting punctuation
    sentence = sentence.split(properNoun.text)
    sentence = sentence[0] + 'how many' + sentence[1] + '?' 
    return sentence 
   
def askWhQuestion(q, sentence):
    
    entity_dict = sentenceNER(sentence)
    questions = [] 
    for properNoun in entity_dict:
        interrogative = entity_dict[properNoun] 
        if interrogative == 'Who':
            questions += generateWhoFromSentence(sentence, properNoun)
        elif interrogative == 'What':
            questions.append(generateWhatFromSentence(sentence, properNoun))
        elif interrogative == 'How many': 
            questions.append(generateHowManyFromSentence(sentence, properNoun)) 
        else:
            questions.append(generateWhenWhereFromQ(q, entity_dict))

        whyQ = generateWhyFromQ(q)
        if whyQ:
            questions.append(whyQ) 

    return questions    


#print(generateWhenWhereFromQ('Did Alan Turing live in England?', {'Alan Turing': 'Who', 'England': 'Where'}))
#print(generateWhenWhereFromQ('Was Alan Turing born in 1915?', {'Alan Turing': 'Who', '1915': 'When'}))
#print(generateWhenWhereFromQ('Is Carnegie Mellon in Pittsburgh, Pennsylvania?', {'Carnegie Mellon': 'What', 'Pittsburgh': 'Where', 'Pennsylvania': 'Where'}))
#print(generateWhoFromSentence('Alan Turing is the father of computer science?', {'Alan Turing': 'Who'}))
#print(generateWhoFromSentence('Alan Turing lived in England.', {'Alan Turing': 'Who', 'England': 'Where'}))
#int(generateWhoFromSentence("Alice said hi, but I forgot to reply.", {'Alice': 'Who', 'I':'Who'}))
#print(generateWhatFromQ('Did Alan Turing like ice cream?'))
#print(generateWhyFromQ('Did Alan Turning like potatoes because they are delicious?'))
#print(askWhQuestion("Did The Guardian suggest that the goal 'might become the most famous goal in Fulham's history'?", "The Guardian suggested that the goal 'might become the most famous goal in Fulham's history'."))
#print(askWhQuestion('Did Alan Turing live in England?', 'Alan Turing lived in England.'))