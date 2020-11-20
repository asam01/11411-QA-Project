# uncomment to suppress warnings about version
import warnings
warnings.filterwarnings("ignore")

#import nltk
import spacy
import benepar
from benepar.spacy_plugin import BeneparComponent

#python -m pip install tensorflow==1.14 will help.
def preprocess(sentence):
    clauses = [] 
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe(BeneparComponent('benepar_en2'))
    doc = nlp(sentence)
    #lowerbound = 0 

    #print(len(list(doc.sents)))
    if len(list(doc.sents)) == 0:
        return clauses
    sent = list(doc.sents)[0]
    children = list(sent._.children)
    puncts = '?!.,;:-'
    for clause in children: 
        if clause.text not in puncts:
            if 'S' in clause._.labels:
                clauses.append((clause.text + '.'))
            
    if not clauses:
        return [sentence]
    else:
        return clauses

# should only enter this function if the root of the syntax
# tree is a VP (verb phrase)
def ask_compound_bin_question(sentence):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)

    # uncomment the next three lines for debugging
    #print('\ndoc: ', doc)
    #for token in doc:
    #    print(token.text, token.pos_, token.dep_, spacy.explain(token.tag_), token.lemma_)
    
    lemmas = []
    correct_do = ''
    subject_explained = ''
    subjects = [] 
    # lemmatize verb
    for token in doc:

        #print('token head type: ', type(token.head.text))
        # TODO: account for all types of subjects
        if 'subj' in token.dep_:
            subj = token.text
            subject_explained = spacy.explain(token.tag_)
            subjects.append(token)
        elif 'conj' in token.dep_ and token.head.text == subj: 
            subjects.append(token.head.text) 
        if token.pos_ == "VERB":
            verb_explained = spacy.explain(token.tag_)

            # TODO: need some way to account for they
            if 'present' in verb_explained:
                #if subj == 'they': 
                if len(subjects)>1: 
                    correct_do = 'Do'
                elif 'plural' in subject_explained:
                    correct_do = 'Do'
                elif 'personal' in subject_explained:
                    correct_do = 'Do'
                elif 'singular' in verb_explained: 
                    correct_do = 'Does'
            # use past tense inflection
            else:
                correct_do = 'Did'
            lemmas.append(token.lemma_)

    #print('lemmas: ', lemmas)

    # construct question
    question = correct_do
    after_subj = False
    # add in subject
    i = 0
    while i < len(doc): 
        token = doc[i]

        if 'subj' in token.dep_:
            if token.pos_ == 'PRON' and token.text != 'I':
                question += ' ' + token.text.lower()
            else:
                question += ' ' + token.text
            after_subj = True
        # account for case of gerund/present participle
        # go + verb-ing
        elif token.pos_ == 'VERB' and 'gerund' not in spacy.explain(token.tag_):
            question += ' ' + lemmas.pop(0) 
        elif token.pos_ == 'DET': 
            question += ' ' + token.text.lower() 
        elif token.pos_ == 'INTJ' and not after_subj: 
            i += 1  

        # end question at punctuation
        elif 'sentence closer' in spacy.explain(token.tag_):
            question += '?'
            break
        else:
            question += ' ' + token.text

        i += 1

    return question

def postprocess (sentences):

    questions = []
    for sentence in sentences:
        questions.append((ask_compound_bin_question(sentence), sentence))

    return questions

def ask_q (sentence):
    sentences = preprocess(sentence)
    questions = postprocess(sentences)
    return questions

'''s4 = 'Unfortunately for their mother, Alice and Bob really hate brussel sprouts.'
print(ask_q(s4))

s5 = 'Alice, who is nice, said hi to me.'
print(ask_q(s5))

s6 = 'Alice said hi, but I forgot to reply.'
print(ask_q(s6))

s7 = 'I went to the store, however, Alice said hello.'
print(ask_q(s7))

s8 = 'Alice ran yesterday.'
print(ask_q(s8))

s9 = 'Alan Turing liked potatoes because they are delicious.'
print(ask_q(s9)) '''