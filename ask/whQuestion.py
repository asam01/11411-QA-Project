import spacy
import benepar
from benepar.spacy_plugin import BeneparComponent
from compoundBinary import preprocess
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
def generateWhenWhereFromQ(question, entity_dict):
    #questions_list = []
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
                    
                    # prioritize when/where questions over who and what
                    question = question.split(stringtotakeout) 
                    question = questionword + ' ' + "".join(question)
                    return question 
        
    


                    
def generateWhoFromSentence(sentence, entity_dict):
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
                for word in entity_dict: 
                    if(entity_dict[word] == 'Who' and word == clause.text): 
                        stringtotakeout = clause.text
                        questionword = entity_dict[word]  
                        question = sent.split(stringtotakeout) 
                        question = questionword + ' ' + "".join(question)
                        questions.append(question[:len(question)-1] + '?')
    
    return questions 


def generateWhatFromQ(question): 
    # Did Alan Turing like ice cream? --> What did Alan Turing like?
    # deal with "what" questions - replace 
    # direct object with "what"
    prevtoken = None 
    doc = nlp(question)
    for token in doc:
        if prevtoken is not None and 'compound' in prevtoken.dep_ and 'obj' in token.dep_:
            stringtotakeout = prevtoken.text + ' ' + token.text        
            questionword = 'What'
            question = question.split(stringtotakeout) 
            question = questionword + ' ' + "".join(question)
            return question 
        elif 'obj' in token.dep_:
            stringtotakeout = token.text        
            questionword = 'What'
            question = question.split(stringtotakeout) 
            question = questionword + ' ' + "".join(question)
            return question    
        

        prevtoken = token
        

    return ""

# Alan Turing liked potatoes because they are delicious.
# --> Did Alan Turning like potatoes because they are delicious?
# --> Why did Alan Turing like potatoes?
def generateWhyFromQ(question):
    words_to_split_on = ['because', 'since', 'due to']
    for word in words_to_split_on: 
        if(word in question): 
            question = question.split(word) 
            question = 'Why ' + question[0] + '?'
            return question  
   


'''print(generateWhenWhereFromQ('Did Alan Turing live in England?', {'Alan Turing': 'Who', 'England': 'Where'}))
print(generateWhenWhereFromQ('Was Alan Turing born in 1915?', {'Alan Turing': 'Who', '1915': 'When'}))
print(generateWhenWhereFromQ('Is Carnegie Mellon in Pittsburgh, Pennsylvania?', {'Carnegie Mellon': 'What', 'Pittsburgh': 'Where', 'Pennsylvania': 'Where'}))
print(generateWhoFromSentence('Alan Turing is the father of computer science?', {'Alan Turing': 'Who'}))
print(generateWhoFromSentence('Alan Turing lived in England.', {'Alan Turing': 'Who', 'England': 'Where'}))
print(generateWhoFromSentence("Alice said hi, but I forgot to reply.", {'Alice': 'Who', 'I':'Who'}))
print(generateWhatFromQ('Did Alan Turing like ice cream?'))'''
print(generateWhyFromQ('Did Alan Turning like potatoes because they are delicious?'))