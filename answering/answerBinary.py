import warnings
warnings.filterwarnings("ignore")

import nltk
from nltk.corpus import wordnet as wn
import spacy
from spacy import displacy
from spacy.pipeline import EntityRecognizer
from collections import Counter
import requests
import re
nlp = spacy.load("en_core_web_sm")

# Given a question and a sentence, check whether the answer is Yes or No
# When do we output a No?
# - different information in a phrase
#   eg. Alan was born in 1915. {Alan: Who, in 1915: When}
#       Q: Was Alan born in 2015? 
#       A: No.
#       Q: Was KT born in 1915?
#       A: No.
# - ODD number of negative words [no, not, never, none...]
# - Antonyms or synonyms present

# input one question, its entity_dict, and a list of top 3 sentences
# output True/False as answer

# determineInterrogative
# who, when, how much, where, what
def sentenceNER(sentence):  
    doc = nlp(sentence)
    entity_dict = {} 
    for ent in doc.ents: 
        entity_dict[ent] = ent.label_

    #print(entity_dict)
    for word in entity_dict:
        tag = entity_dict[word]

        if tag == 'PERSON':
            entity_dict[word] = 'Who'

        elif tag == 'DATE' or tag == "TIME":
            entity_dict[word] = 'When'

        elif tag == "MONEY":
            entity_dict[word] = "How much"
        
        elif tag == 'LOC' or tag == 'GPE': 
            entity_dict[word] = "Where" 
        
        else:
            entity_dict[word] = "What"
            
    return entity_dict   

# This function answers a simple binary question using the top
# 3 relevant sentences found using function find_sentence(question, corpus);
def answerBinary(question, sentList):
    qEntityDict = sentenceNER(question)
    # print("qEntityDict", qEntityDict)
    lenSenList = len(sentList)
    result = [True]*lenSenList
    negations = {"no", "not", "never", "none", "no one", "nobody", "nothing", "neither", "nowhere", "hardly", "scarcely", "barely", "isn't", "wasn't", "shouldn't", "wouldn't", "couldn't", "cannot", "can't", "won't", "don't", "doesn't", "didn't"}

    for index in range(lenSenList):
        sent = sentList[index]
        sentEntityDict = sentenceNER(sent)
        # print("sentEntityDict", sentEntityDict)
        # sentTagDict is the reverse of entity dict
        # for each sentence, we need to compare the phrase with the same tag
        # to check whether the information is correct
        sentTagDict = dict() #{tag: [phrases]}
        for item in sentEntityDict:
            phrase = item
            tag = sentEntityDict[item]
            if tag not in sentTagDict:
                sentTagDict[tag] = [phrase]
            else:
                sentTagDict[tag] += [phrase]
        # print("sentTagDict", sentTagDict)
        # for every text:tag pair in question
        # check whether there is the same text in the sentence (from a list of phrases of the same tag)
        for phrase in qEntityDict:
            tag = qEntityDict[phrase]
            if tag in sentTagDict: # dont count for any phrases with tag not contained in the sentence
                # we can only compare strings, but not spacy tags
                tempCount = 0
                for item in sentTagDict[tag]:
                    if str(phrase) == str(item):
                        tempCount += 1
                if tempCount == 0:
                    result[index] = False
        # print("result", result)

        # count number of negations
        # is number of nagations is odd, turn True to False, turn False to true
        sentWords = sent.split()
        qWords = question.split()
        count = 0
        for word in sentWords:
            if word in negations:
                count += 1
        for word in qWords:
            if word in negations:
                count += 1
        if count % 2 == 1:
            result[index] = not result[index]
        # print("result", result)

    trueCount = result.count(True)
    # print("trueCount", trueCount)
    if trueCount >= (lenSenList/2):
        return "Yes."
    else:
        return "No."

s1 = "Alan Turing was born in 1915."
q1_Yes = "Was Alan Turing born in 1915?"
q1_No = "Is Alan Turing born in 2020?"
# print(answerBinary(q1_Yes, [s1]))
# print(answerBinary(q1_No, [s1]))

s2 = 'Bob said hi to me.'
q2_Yes = "Did Bob say hi to me?"
q2_No = "Did Neil say hi to me?"
# print(answerBinary(q2_Yes, [s2]))
# print(answerBinary(q2_No, [s2]))

s3 = 'Unfortunately for their mother, Alice and Bob really hate brussel sprouts.'
q3_Yes = "Do Alice and Bob hate brussel sprouts?"
q3_No = "Do Alice and Bob not hate brussel sprouts?"
# print(answerBinary(q3_Yes, [s3]))
# print(answerBinary(q3_No, [s3]))


