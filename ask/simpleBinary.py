import nltk
from nltk.tokenize import word_tokenize
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
                # directly return here, hence will only produce 1 question for each sentence for now
                result.append((newSentence + "?", sentence))

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
                result.append((newSentence + "?", sentence))
    
    return result

'''
things to do:
- add in name entity to distinguish which are the word that needs to keep capitalized
- process punctuation (QUESTION: HOW IS PUNCTUATION PROCESSED IN TOKENIZE?)
    - if punctuation is treated as an individual word with space on both sides:
        - detect punction, delete the space before punctuation, leave the space after punctuation
    - else...?
'''

''''s1 = "Gyarados (Gyaradosu) is a Pokémon species in Nintendo and Game Freak's Pokémon franchise."
s2 = "Created by Ken Sugimori, Gyarados first appeared in the video games Pokémon Red and Pokemon Green and subsequent sequels, later appearing in various merchandise, spinoff titles and animated and printed adaptations of the franchise. "
s3 = "Lesley should be doing her homework."
s4 = "This is a good idea."
s5 = "Just a random sentence."
s6 = "I must go."
input = [s1, s2, s3, s4, s5, s6]
result = simpleBinary(input)
print(result)'''

