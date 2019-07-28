from bs4 import BeautifulSoup
from collections import defaultdict
import heapq
import math
import nltk
import requests
import re

def gather_text(country):
    """extract all texts in wikipedia for given country"""
    url = f'https://en.wikipedia.org/wiki/{country}'
    response = requests.get(url)
    # grab every thing as a text and parse it.
    soup = BeautifulSoup(response.text, 'html.parser')

    # all texts are embedded within <p> tags for any wikipedia article
    paragraphs = soup.find_all("p")
    article = ""
    for p in paragraphs:
        article += p.text # only grabbing text inside <p> tags

    sentences = nltk.sent_tokenize(article)
    return sentences

def cleanSentence(sent):
    """
    1. Get rid of string that match pattern: "[numbers]"
    2. Replace anything other than number or alphabet(lower + upper)
    3. Get rid of white spaces into single one.
    """
    cleaned_sentence = re.sub(r'\[[0-9]*\]', ' ', sent)
    cleaned_sentence = re.sub("[^a-zA-Z1-9]", " ", cleaned_sentence)
    cleaned_sentence = re.sub(r'\s+', ' ', cleaned_sentence)
    
    return cleaned_sentence

def create_freq_matrix(sentences):
    """
    for each sentence count number of instances for each word within a sentence.
    it is a dictionary containing {sentence: freq_table} where 
    freq_table = {"word1": count, "word2": count,...etc.}
    """
    freq_matrix = {}
    stopwords = nltk.corpus.stopwords.words('english')
    ps = nltk.PorterStemmer()
    for sent in sentences:
        freq_table = defaultdict(lambda: 0) # new dict for each sentence
        
        # break sentences down to words
        for word in nltk.word_tokenize(sent):
            word = ps.stem(word.lower())
            if word in stopwords: # skipping stopwords
                continue # stop here and goto next iteration
            freq_table[word] += 1
            
        freq_matrix[sent] = dict(freq_table)
        
    return freq_matrix

def create_tf_matrix(freq_matrix):
    """ 
    same as freq_matrix however instead of count, 
    it will have Term Frequency value.

    ex: tf_matrix = {sentence: {"korea": tf_value, "canada": tf_value},
                     sentence2: {"hello":tf_value, "hi":tf_value}}

    Fomula for term frequency = number of targer word in sentence/ total number of words
    """
    tf_matrix = {}
    for sent, f_table in freq_matrix.items():
        tf_table = {}
        all_words_count = len(f_table)
        for word, target_count in f_table.items():
            tf_table[word] = target_count/all_words_count 
            
        # insert new tf_table(dict) into tf_matrix dictionary
        tf_matrix[sent] = tf_table
        
    return tf_matrix

def create_documents_per_word(freq_matrix):
    """
    finding number of sentences target word appeared in.
    lower the better => rare.
    Creating one huge dictionary instead of creating new one each loop to
    include all sentences
    """
    words_per_doc_table = defaultdict(lambda:0)
    
    for sent, f_table in freq_matrix.items():
        for word, count in f_table.items():
            words_per_doc_table[word] += 1 
            
    return dict(words_per_doc_table) # chaning back to dictionary from default dictionary just b.c. it looks cleaner.

def create_idf_matrix(freq_matrix, documents_per_word, total_docs):
    """ 
    just like tf_matrix but vavlue is Inverse document frequency value.
    """
    idf_matrix = {}
    for sent, f_table in freq_matrix.items():
        idf_table = {}
        for word in f_table.keys():
            idf_table[word] = math.log10(total_docs / (documents_per_word[word]))
        idf_matrix[sent] = idf_table

    return idf_matrix

def create_tfidf_matrix(tf_matrix, idf_matrix):
    """
    Multiply TF*IDF for each word.
    
    Note:   sent1, sent2 are the same.
            word1,2 are the same.
            value1 = TF score for current word
            value2 = IDF score for current word     
    """
    tfidf_matrix = {}   
    for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):
        tfidf_table = {}        
        for (word1, value1), (word2, value2) in zip(f_table1.items(),
                                                   f_table2.items()):
            tfidf_table[word1] = float(value1 * value2)

        tfidf_matrix[sent1] = tfidf_table
    return tfidf_matrix

def SentenceScore(tfidf_matrix):
    """
    For each sentence add up tfidf scores but since sentences have different
    length, divide total_score_per_setence by total_words_in_sentence.
    """
    sentence_score = {}
    for sent, f_table in tfidf_matrix.items():
        total_score_per_sentence = 0
        total_words_in_sentence = len(f_table)
        
        for score in f_table.values():
            total_score_per_sentence += score

        sentence_score[sent] = total_score_per_sentence / total_words_in_sentence
    
    return sentence_score

def AverageScore(sentence_score):
    """
    Average score will be the threshold point => if sentence has score above it, it will
    be included into summary
    """
    sum_value = 0
    for entry in sentence_score: # only keys
        sum_value += sentence_score[entry] # dictionary of {sentence: score,...etc.}
    
    average = (sum_value/len(sentence_score))
    
    return average

def summarize(sentences, sentence_score, threshold):
    """
    With given threshold summarize with sentences that are above threshold.
    Each sentence will be joined by ". " and period at the end, it will be returned as one string
    """
    sentences = [sentence.strip() for sentence in sentences if sentence in sentence_score and sentence_score[sentence] >= threshold]
    summary = ". ".join(sentences) + "."
    # print(f'from {total_docs} sentences summarized to {sentence_count} sentences with threshold point of {threshold}')
    return summary