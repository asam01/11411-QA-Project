# NOTE: for relative imports to work, run this from the '11411-QA-Project' directory

from preprocess.tokenize import convertPronoun2Noun
from preprocess.findImportantSentences import run_summarization 
from ask.compoundBinary import ask_q
#from ask.simpleBinary import 
import sys
import io

# step 4: generate binary questions 

# step 5: run binary questions through preprocessor (determine interrogative)

# step 6: generate wh- questions

# step 7: rank & output to console



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 ask.py article.txt nquestions")
        sys.exit(1)

    article = sys.argv[1]
    nquestions = sys.argv[2]

    # step 1: take txt file as input 
    with io.open(article, 'r', encoding='utf8') as f:
        article_string = f.read()

    # step 2: tokenize & convert pronouns to nouns
    preprocessed_article = convertPronoun2Noun(article_string)

    # step 3: summarize text file (important sentences)
    summary_text = run_summarization(preprocessed_article, nquestions) 
    tokenized_summary = str.split('\n')
    




