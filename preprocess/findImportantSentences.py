# this is adapted from https://github.com/akashp1712/nlp-akash/blob/master/text-summarization/TF_IDF_Summarization.py
from __future__ import unicode_literals, print_function
import spacy 
from spacy.lang.en import English
import warnings
warnings.filterwarnings("ignore")

import math
import nltk
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords
import re
# fine tune these parameters later
#NUM_SENTENCES = 5
DISCOUNT_FACTOR = .95


def _create_frequency_table(text_string) -> dict:
    """
    we create a dictionary for the word frequency table.
    For this, we should only use the words that are not part of the stopWords array.
    Removing stop words and making frequency table
    Stemmer - an algorithm to bring words to its root word.
    :rtype: dict
    """
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text_string)
    ps = PorterStemmer()

    freqTable = dict()
    for word in words:
        word = ps.stem(word)
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    return freqTable


def _create_frequency_matrix(sentences):
    frequency_matrix = {}
    stopWords = set(stopwords.words("english"))
    ps = PorterStemmer()

    for sent in sentences:
        freq_table = {}
        words = word_tokenize(sent)
        for word in words:
            word = word.lower()
            word = ps.stem(word)
            if word in stopWords:
                continue

            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1

        frequency_matrix[sent[:15]] = freq_table

    return frequency_matrix


def _create_tf_matrix(freq_matrix):
    tf_matrix = {}

    for sent, f_table in freq_matrix.items():
        tf_table = {}

        count_words_in_sentence = len(f_table)
        for word, count in f_table.items():
            tf_table[word] = count / count_words_in_sentence

        tf_matrix[sent] = tf_table

    return tf_matrix


def _create_documents_per_words(freq_matrix):
    word_per_doc_table = {}

    for sent, f_table in freq_matrix.items():
        for word, count in f_table.items():
            if word in word_per_doc_table:
                word_per_doc_table[word] += 1
            else:
                word_per_doc_table[word] = 1

    return word_per_doc_table


def _create_idf_matrix(freq_matrix, count_doc_per_words, total_documents):
    idf_matrix = {}

    for sent, f_table in freq_matrix.items():
        idf_table = {}

        for word in f_table.keys():
            idf_table[word] = math.log10(total_documents / float(count_doc_per_words[word]))

        idf_matrix[sent] = idf_table

    return idf_matrix


def _create_tf_idf_matrix(tf_matrix, idf_matrix):
    tf_idf_matrix = {}

    for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):

        tf_idf_table = {}

        for (word1, value1), (word2, value2) in zip(f_table1.items(),
                                                    f_table2.items()):  # here, keys are the same in both the table
            tf_idf_table[word1] = float(value1 * value2)

        tf_idf_matrix[sent1] = tf_idf_table

    return tf_idf_matrix


def _score_sentences(tf_idf_matrix) -> dict:
    """
    score a sentence by its word's TF
    Basic algorithm: adding the TF frequency of every non-stop word in a sentence divided by total no of words in a sentence.
    :rtype: dict
    """

    sentenceValue = {}

    for sent, f_table in tf_idf_matrix.items():
        total_score_per_sentence = 0

        count_words_in_sentence = len(f_table)
        for word, score in f_table.items():
            total_score_per_sentence += score

        sentenceValue[sent] = total_score_per_sentence / count_words_in_sentence

    return sentenceValue


def _find_average_score(sentenceValue) -> int:
    """
    Find the average score from the sentence value dictionary
    :rtype: int
    """
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # Average value of a sentence from original summary_text
    average = (sumValues / len(sentenceValue))

    return average


def _generate_summary(sentences, sentenceValue, threshold, num_sentences):
    sentence_count = 0
    summary = ''
    # extend to output a certain number of sentences. 
    for sentence in sentences:
        if sentence[:15] in sentenceValue and sentenceValue[sentence[:15]] >= (threshold):
            summary += (sentence + "\n")
            sentence_count += 1

    if sentence_count < num_sentences:
       return _generate_summary(sentences, sentenceValue, threshold * DISCOUNT_FACTOR, num_sentences)

    return summary


def run_summarization(text, num_sentences):
    """
    :param text: Plain summary_text of long article
    :return: summarized summary_text
    """

    '''
    We already have a sentence tokenizer, so we just need 
    to run the sent_tokenize() method to create the array of sentences.
    '''
    # 1 Sentence Tokenize
    #sentences = re.split('. |?|!', text)
    #sentences = nltk.tokenize.sent_tokenize(text)
 
    #nlp = English()
    nlp = spacy.load('en_core_web_sm', disable = ['ner', 'parser', 'tagger'])
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    doc = nlp(text)
    sentences = [sent.string.strip() for sent in doc.sents]
    total_documents = len(sentences)
    #print(sentences)

    # 2 Create the Frequency matrix of the words in each sentence.
    freq_matrix = _create_frequency_matrix(sentences)
    #print(freq_matrix)

    '''
    Term frequency (TF) is how often a word appears in a document, divided by how many words are there in a document.
    '''
    # 3 Calculate TermFrequency and generate a matrix
    tf_matrix = _create_tf_matrix(freq_matrix)
    #print(tf_matrix)

    # 4 creating table for documents per words
    count_doc_per_words = _create_documents_per_words(freq_matrix)
    #print(count_doc_per_words)

    '''
    Inverse document frequency (IDF) is how unique or rare a word is.
    '''
    # 5 Calculate IDF and generate a matrix
    idf_matrix = _create_idf_matrix(freq_matrix, count_doc_per_words, total_documents)
    #print(idf_matrix)

    # 6 Calculate TF-IDF and generate a matrix
    tf_idf_matrix = _create_tf_idf_matrix(tf_matrix, idf_matrix)
    #print(tf_idf_matrix)

    # 7 Important Algorithm: score the sentences
    sentence_scores = _score_sentences(tf_idf_matrix)
    #print(sentence_scores)

    # 8 Find the threshold
    threshold = _find_average_score(sentence_scores)
    #print(threshold)

    # 9 Important Algorithm: Generate the summary
    summary = _generate_summary(sentences, sentence_scores, 1.3 * threshold, num_sentences)

    # splice off beginning and end empty lines
    summary = summary.strip() 
    return summary

text_str = '''
Carnegie Mellon University (CMU) is a private research university based in Pittsburgh, Pennsylvania.
Founded in 1900 by Andrew Carnegie as the Carnegie Technical Schools, the university became the Carnegie Institute of Technology in 1912 and began granting four-year degrees.
In 1967, the Carnegie Institute of Technology merged with the Mellon Institute of Industrial Research, formerly a part of the University of Pittsburgh, to form Carnegie Mellon University.
With its main campus located 3 miles (5 km) from Downtown Pittsburgh, Carnegie Mellon has grown into an international university with over a dozen degree-granting locations in six continents, including campuses in Qatar and Silicon Valley, and more than 20 research partnerships.
The university has seven colleges and independent schools, all of which offer interdisciplinary programs: the College of Engineering, College of Fine Arts, Dietrich College of Humanities and Social Sciences,
Mellon College of Science, Tepper School of Business, H. John Heinz III College of Information Systems and Public Policy, and the School of Computer Science.
Carnegie Mellon counts 14,799 students from 117 countries, over 109,000 living alumni, and over 1,400 faculty members.
Past and present faculty and alumni include 20 Nobel Prize laureates, 13 Turing Award winners, 23 Members of the American Academy of Arts and Sciences, 
22 Fellows of the American Association for the Advancement of Science, 79 Members of the National Academies, 124 Emmy Award winners, 47 Tony Award laureates, and 10 Academy Award winners.
The Carnegie Technical Schools were founded in 1900 in Pittsburgh by the Scottish American industrialist and philanthropist Andrew Carnegie, who wrote the time-honored words "My heart is in the work", 
when he donated the funds to create the institution. Carnegie's vision was to open a vocational training school for the sons and daughters of working-class Pittsburghers (many of whom worked in his mills).
Carnegie was inspired for the design of his school by the Pratt Institute in Brooklyn, New York founded by industrialist Charles Pratt in 1887. In 1912, the institution changed its name to Carnegie Institute of Technology (CIT)
and began offering four-year degrees. During this time, CIT consisted of four constituent schools: the School of Fine and Applied Arts, the School of Apprentices and Journeymen, the School of Science and Technology,
and the Margaret Morrison Carnegie School for Women.
The Mellon Institute of Industrial Research was founded in 1913 by banker and industrialist brothers Andrew Mellon (who went on to become U.S. Treasury Secretary)
and Richard B. Mellon in honor of their father, Thomas Mellon, patriarch of the Mellon family. 
The Institute began as a research organization which performed work for government and industry on a contract and was initially established as a department within the University of Pittsburgh.
In 1927, the Mellon Institute incorporated as an independent nonprofit. In 1937, the Mellon Institute's iconic building was completed and it moved to its new, and current, location on Fifth Avenue.'''

#x = run_summarization(text_str,5) 
#print(x)
