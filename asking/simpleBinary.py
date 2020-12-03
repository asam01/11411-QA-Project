import warnings
warnings.filterwarnings("ignore")

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.tag import pos_tag
import string

# after tokenize the input is a list of strings
# each string is a complete sentence

''' create a list of all "to be" verbs
Sentence: A 'to_be' B eg. KT is tired.
Question: 'to_be' A B? eg. Is KT tired?
Rules: 
- pull out 'to_be' verb and insert to the front
- Adjust 1st letter of "to_be" & 1st letter of original sentence
'''
to_be = ['am', 'is', 'are', 'was', 'were']

'''
 create a list of aux_verb 
 Sentence: A "aux_verb" infinitive_verb_phase eg. KT must sleep.
 Question: "aux_verb" A infinitive_verb_phase? eg. Must KT sleep?
 * The question could also be "What must KT do?", but for the sake of simplicity we do binary first
 Rules: 
- pull out 'aux_verb' and insert to the front
- Adjust 1st letter of "aux_verb" & 1st letter of original sentence
'''
aux_verb = ['must', 'can', 'could', 'shall', 'should', 'will', 'would', 'may', 'might']

def ask_simple_binary(input):
    result = []
    for sentence in input:
        words = sentence.split()
        # check "to_be" verbs
        # ignore complex sentence structure first
        # find at most 1 question for each sentence
        for beV in to_be:
            # "to_be" case
            if beV in words:
                words.remove(beV)
                # edge case: words that must be capitalized
                # need to add more, such as name entities
                if words[0] not in ["I"]: 
                    words[0] = words[0][0].lower() + words[0][1:]
                beVCap = beV[0].upper() + beV[1:]
                newSentence = beVCap + ' ' + ' '.join(words)

                # remove existing punctuation
                newSentence = newSentence[:(len(newSentence)-1)]
                # directly return here, hence will only produce 1 question for each sentence for now
                result.append((newSentence + "?", sentence))
                '''
                wordNetQns = useWordNet(newSentence)
                for qn in wordNetQns:
                    result.append((qn + "?", sentence))
                '''

        for auxV in aux_verb:
            if auxV in words:
                words.remove(auxV)
                # edge case: words that must be capitalized
                # need to add more, such as name entities
                if words[0] not in ["I"]: 
                    words[0] = words[0][0].lower() + words[0][1:]
                auxVCap = auxV[0].upper() + auxV[1:]
                newSentence = auxVCap + ' ' + ' '.join(words)
                # directly return here, hence will only produce 1 question for each sentence for now
                '''
                result.append((newSentence + "?", sentence))
                wordNetQns = useWordNet(newSentence)
                for qn in wordNetQns:
                    result.append((qn + "?", sentence))
                '''
    return result

'''
def useWordNet(newSentence):
    ss = nltk.tokenize.sent_tokenize(newSentence)
    tokenized_sent=[nltk.tokenize.word_tokenize(sent) for sent in ss]
    pos_sentences=[nltk.pos_tag(sent) for sent in tokenized_sent]
    result = []
    for i in pos_sentences[0]:
        word = i[0]
        # https://opensenselabs.com/blog/tech/entity-extraction-using-nlp-python
        if i[1] == 'NN':
            hypernyms = []
            for syn in wn.synsets(word):
                if syn.hypernyms():
                    hypernyms.append(syn.hypernyms()[0].name().split(".")[0])
        
            if hypernyms != []:
                hyper = hypernyms[0]
                if hyper.lower() != word.lower():
                    temp = newSentence.replace(word, hyper)
                    result += [temp]
        

        if i[1] in ['NN', 'JJ', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'] and word.lower() not in to_be:
            synonyms = []
            antonyms = []


            for syn in wn.synsets(word):
                for l in syn.lemmas():
                    synonyms.append(l.name())
                    if l.antonyms():
                        antonyms.append(l.antonyms()[0].name())
                    
            
            # Only get the TOP ONE synonyms and antonyms and create questions. 
            # If top synonym is the word itself, ignore; if no antonym, ignore. 
            if synonyms != []:
                syn = synonyms[0]
                if syn.lower() != word.lower():
                    temp = newSentence.replace(word, syn)
                    result += [temp]

            if antonyms != []:
                ant = antonyms[0]
                temp = newSentence.replace(word, ant)
                result += [temp]
 

    return result
'''


'''
things to do:
- add in name entity to distinguish which are the word that needs to keep capitalized
- process punctuation (QUESTION: HOW IS PUNCTUATION PROCESSED IN TOKENIZE?)
    - if punctuation is treated as an individual word with space on both sides:
        - detect punction, delete the space before punctuation, leave the space after punctuation
    - else...?
'''

'''
s1 = "Gyarados (Gyaradosu) is a Pokémon species in Nintendo and Game Freak's Pokémon franchise."
s2 = "Created by Ken Sugimori, Gyarados first appeared in the video games Pokémon Red and Pokemon Green and subsequent sequels, later appearing in various merchandise, spinoff titles and animated and printed adaptations of the franchise. "
s3 = "Lesley should be doing her homework."
s4 = "This is a good idea."
s5 = "Just a random sentence."
s6 = "I must go."
s7 = "My dog is cute."
input = [s1, s2, s3, s4, s5, s6, s7]
result = ask_simple_binary(input)
print(result)

[("Is gyarados (Gyaradosu) a Pokémon species in Nintendo and Game Freak's Pokémon franchise?", 
    "Gyarados (Gyaradosu) is a Pokémon species in Nintendo and Game Freak's Pokémon franchise."), 
("Is gyarados (Gyaradosu) a Pokémon species in Nintendo and Game Freak's Pokémon concession?", 
    "Gyarados (Gyaradosu) is a Pokémon species in Nintendo and Game Freak's Pokémon franchise."), 

('Should lesley be doing her homework.?', 'Lesley should be doing her homework.'), 
('Should lesley be make her homework.?', 'Lesley should be doing her homework.'), 
('Should lesley be unmake her homework.?', 'Lesley should be doing her homework.'), 
('Should lesley be doing her school_assignment.?', 'Lesley should be doing her homework.'), 

('Is this a good idea?', 'This is a good idea.'), 
('Is this a evil idea?', 'This is a good idea.'), 
('Is this a good content?', 'This is a good idea.'), 

('Must I go.?', 'I must go.'), 
('Must I stay_in_place.?', 'I must go.'), 

('Is my apple red?', 'My apple is red.'), 
('Is my edible_fruit red?', 'My apple is red.'), 
('Is my apple gain?', 'My apple is red.')]

'''