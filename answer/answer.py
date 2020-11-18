import spacy
import benepar
from benepar.spacy_plugin import BeneparComponent
import reverseAsk
import answerBinary
import find_sentence
import sys 
import io 


nlp = spacy.load("en_core_web_sm")
nlp.add_pipe(BeneparComponent('benepar_en2'))
    
# uncomment to suppress warnings about version
import warnings
warnings.filterwarnings("ignore")

def answerMain(question, corpus):
    qnWord = question.split(" ")[0]
    sentenceList = find_sentence(question, corpus)
    if qnWord in ["who", "where", "which", "how much", "when"]:
        answersList = reverseAsk.answerWh(question, sentenceList)
    elif qnWord == "what":
        answersList = reverseAsk.answerWh(question, sentenceList)
    else: answersList = answerBinary(question, sentenceList)
    return answersList

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 answer.py article.txt questions.txt")
        sys.exit(1)

    article = sys.argv[1]
    questions = (sys.argv[2])
    
    article_string = ""
    questions_string = "" 
    with io.open(article, 'r', encoding='utf8') as f:
        article_string = f.read()
    with io.open(questions, 'r', encoding='tuf8') as f: 
        questions_string = f.read() 
    qs = questions_string.split("\n")

    answers = [] 
    for q in qs:
        answers += answerMain(q, article_string) 
    # output to stdout  
    for a in answers: 
        print(a)




