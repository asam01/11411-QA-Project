from os import set_inheritable
import warnings
warnings.filterwarnings("ignore")

import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords 
import numpy as np

# adapted from: https://www.geeksforgeeks.org/python-measure-similarity-between-two-sentences-using-cosine-similarity/
def cosineSim(sentence, question):
    # Program to measure the similarity between  
    # two sentences using cosine similarity. 

    X = sentence
    Y = question
  
    # tokenization 
    X_list = X.split() 
    Y_list = Y.split() 
  
    # sw contains the list of stopwords 
    sw = stopwords.words('english')  
    l1 =[]
    l2 =[] 
  
    # remove stop words from the string 
    X_set = {w for w in X_list if not w in sw}  
    Y_set = {w for w in Y_list if not w in sw} 
  
    # form a set containing keywords of both strings  
    rvector = X_set.union(Y_set)  
    for w in rvector: 
        if w in X_set: l1.append(1) # create a vector 
        else: l1.append(0) 
        if w in Y_set: l2.append(1) 
        else: l2.append(0) 
    c = 0

    # cosine formula  
    for i in range(len(rvector)): 
        c += l1[i]*l2[i] 
    if((sum(l1)*sum(l2))**0.5==0):
        return 0 
    cosine = c / float((sum(l1)*sum(l2))**0.5) 
    return cosine

# This function is to take in a question and a corpus, and outputs 
# top three relevant sentences that might contain answers in the given corpus. 
def find_sentence(question, corpus):
    good_tags = ["NN", "NNS", "NNP", "NNPS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    high_score = 3
    low_score = 1
    q_tags = nltk.pos_tag(word_tokenize(question))
    score_list = []

    for sentence in corpus:
        score_list.append(cosineSim(sentence,question))

    max_score_index = np.argmax(score_list)
    return corpus[max_score_index]

q1 = "Is thermal conductivity of a material a measure of its ability to conduct heat?"
q2 = "Is thermal conductivity a measure?"
q3 = "What is thermal resistivity?"
q4 = "What is the most general form of thermal conductivity?"
q5 = "Who is KT?"

raw = "The thermal conductivity of a material is a measure of its ability to conduct heat.\n Heat transfer occurs at a lower rate in materials of low thermal conductivity than in materials of high thermal conductivity.\nFor instance, metals typically have high thermal conductivity and are very efficient at conducting heat, while the opposite is true for insulating materials like Styrofoam.\nCorrespondingly, materials of high thermal conductivity are widely used in heat sink applications, and materials of low thermal conductivity are used as thermal insulation.\nThe reciprocal of thermal conductivity is called thermal resistivity.\nThis is known as Fourier's Law for heat conduction. \n Although commonly expressed as a scalar, the most general form of thermal conductivity is a second-rank tensor.\nHowever, the tensorial description only becomes necessary in materials which are anisotropic."