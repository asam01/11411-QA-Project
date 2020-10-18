import nltk
import spacy 

# should only enter this function if the root of the syntax
# tree is a VP (verb phrase)
def ask_compound_bin_question(sentence):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)

    # uncomment the next two lines for debugging
    #for token in doc:
    #    print(token.text, token.pos_, token.dep_, spacy.explain(token.tag_), token.lemma_)
    
    lemma = ''
    correct_do = ''
    exp = ''
    # lemmatize verb
    for token in doc:

        # TODO: account for all types of subjects
        if 'subj' in token.dep_:
            subj = token.text.lower() 
            exp = spacy.explain(token.tag_)
  
        if token.pos_ == "VERB":
            explained = spacy.explain(token.tag_)

            if subj == 'they': 
                correct_do = 'Do'
            elif('plural' in exp):
                correct_do = 'Do'
            elif 'present' in explained:
                if 'singular' in explained: 
                    correct_do = 'Does'
                else: 
                    correct_do = 'Do'
            # use past tense inflection
            else:
                correct_do = 'Did'
            lemma = token.lemma_

            break

    # construct question
    question = correct_do

    # add in subject
    for token in doc: 

        if 'subj' in token.dep_:
            if token.pos_ == 'PRON':
                question += ' ' + token.text.lower()
            else:
                question += ' ' + token.text
        elif(token.pos_ == 'VERB'):
            question += ' ' + lemma 
        elif(token.pos_ == 'DET'): 
            question += ' ' + token.text.lower() 
        
      # end question at punctuation
        elif token.pos_ == 'PUNCT':
            question += '?'
            break
        else:
            question += ' ' + token.text

    return question

print(ask_compound_bin_question('Boys run every day.'))