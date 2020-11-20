import warnings
warnings.filterwarnings("ignore")

import nltk
from nltk import pos_tag, word_tokenize
import numpy as np


# This function is to take in a question and a corpus, and outputs 
# top three relevant sentences that might contain answers in the given corpus. 
def find_sentence(question, corpus):
    good_tags = ["NN", "NNS", "NNP", "NNPS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    high_score = 3
    low_score = 1
    q_tags = nltk.pos_tag(word_tokenize(question))
    score_list = []
    corpus = corpus.split("\n")

    for sentence in corpus:
        score = 0
        tags = nltk.pos_tag(word_tokenize(sentence))
        tag_dict = dict()

        #construct dict
        for pair in tags:
            word = pair[0].lower()
            tag = pair[1]
            if tag not in tag_dict:
                tag_dict[tag] = [word]
            else:
                tag_dict[tag].append(word)
        #print(tag_dict)

        #loop question
        for q_pair in q_tags:
            q_word = q_pair[0].lower()
            q_tag = q_pair[1]

            if (q_tag in tag_dict):
                if (q_word in tag_dict[q_tag]):
                    if q_tag in good_tags:
                        score += high_score
                    else:
                        score += low_score

        score_list.append(score)
    
    max_score = max(score_list)
    sentence_list = []
    for index in range(len(score_list)):
        if score_list[index] == max_score:
            sentence_list.append(corpus[index])
    # max_index = score_list.index(max(score_list))
    # best_sentence = corpus[max_index]
    return sentence_list


q1 = "Is thermal conductivity of a material a measure of its ability to conduct heat?"
q2 = "Is thermal conductivity a measure?"
q3 = "What is thermal resistivity?"
q4 = "What is the most general form of thermal conductivity?"
q5 = "Who is KT?"

raw = "The thermal conductivity of a material is a measure of its ability to conduct heat.\n Heat transfer occurs at a lower rate in materials of low thermal conductivity than in materials of high thermal conductivity.\nFor instance, metals typically have high thermal conductivity and are very efficient at conducting heat, while the opposite is true for insulating materials like Styrofoam.\nCorrespondingly, materials of high thermal conductivity are widely used in heat sink applications, and materials of low thermal conductivity are used as thermal insulation.\nThe reciprocal of thermal conductivity is called thermal resistivity.\nThis is known as Fourier's Law for heat conduction. \n Although commonly expressed as a scalar, the most general form of thermal conductivity is a second-rank tensor.\nHowever, the tensorial description only becomes necessary in materials which are anisotropic."
corpus = raw.splitlines()