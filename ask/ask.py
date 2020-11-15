# NOTE: for relative imports to work, run this from the '11411-QA-Project' directory
import sys
import io

#sys.path.append('./preprocess')
#from preprocess import tokenize 
#from tokenize import convertPronoun2Noun
#from findImportantSentences import run_summarization
#from .preprocess.findImportantSentences import run_summarization 

#from compoundBinary import ask_q
#from simpleBinary import simpleBinary 
#from whQuestion import askWhQuestion
#import ask_q, simpleBinary, askWhQuestion
#from .ask.compoundBinary import ask_q
#from .ask.simpleBinary import simpleBinary 
#from .ask.whQuestion import askWhQuestion

 
import compoundBinary 
import simpleBinary 
import whQuestion 
sys.path.append('./preprocess')
import preprocessNER
import findImportantSentences


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 ask.py article.txt nquestions")
        sys.exit(1)

    article = sys.argv[1]
    nquestions = int(sys.argv[2])
    
    print('step1')
    # step 1: take txt file as input 
    article_string = ""
    with io.open(article, 'r', encoding='utf8') as f:
        article_string = f.read()
    print('step2')
    # step 2: tokenize & convert pronouns to nouns
    preprocessed_article = preprocessNER.convertPronoun2Noun(article_string)
    #print("preprocessed article: ", preprocessed_article)
    print('step3')
    # step 3: summarize text file (important sentences)
    summary_text = findImportantSentences.run_summarization(preprocessed_article, nquestions)
    print("summary text: ", summary_text) 
    tokenized_summary = summary_text.split('\n')
    print("tokenized summary: ", tokenized_summary)
    print('step4')
    # step 4: generate binary questions 
    # simple binary 
    simple_binary_questions = simpleBinary.ask_simple_binary(tokenized_summary)
    cb_input = tokenized_summary 
    for (q,s) in simple_binary_questions: 
        for sent in tokenized_summary: 
            if(s==sent): 
                cb_input.remove(sent) 

    print('simple binary: ', simple_binary_questions)
    # compound binary
    compound_binary = []  
    for sent in cb_input:
        for (q,s) in compoundBinary.ask_q(sent):  
            compound_binary.append((q,s)) 

    print('compound binary: ', compound_binary)
    binary_questions = compound_binary + simple_binary_questions
    print('all qs: ', binary_questions )
    wh_questions = [] 
    # step 5: generate wh- questions
    for (q,s) in binary_questions:
        wh_questions.append(whQuestion.askWhQuestion(q,s))
    

    # step 7: rank & output to console
    print(wh_questions)

    ## NOTE: what questions seem to be problematic





