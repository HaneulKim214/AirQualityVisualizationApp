from summarize_text_methods import *

def text_summarizer(country):
    """
    for given country, read its wikipedia and return summarized version.
    It rendered to html.
    Create two versions if time.
    1. nlp
    2. leveraging DL/ML
    """
    # organize text from wikipedia and create tokenize to list of sentence
    sentences = gather_text(country)
    total_sentences = len(sentences)
    sentences = [cleanSentence(sent) for sent in sentences] #clean each sentence and store back into a list.
    
    # create freq_matrix
    freq_matrix = create_freq_matrix(sentences)

    # creating all matrix created with freq_matrix
    tf_matrix = create_tf_matrix(freq_matrix)
    documents_per_word = create_documents_per_word(freq_matrix)

    # IDF matrix.
    idf_matrix = create_idf_matrix(freq_matrix, documents_per_word, total_sentences)

    # Multiply TF*IDF scores for each word and again create a matrix.
    tfidf_matrix = create_tfidf_matrix(tf_matrix, idf_matrix)

    # Assign score to each sentence
    sentence_score = SentenceScore(tfidf_matrix)

    # set threshold point
    threshold = AverageScore(sentence_score)

    # Finally summarize, I've increase threshold by 1.7x to create short and strong summary
    summarized_text = summarize(sentences, sentence_score, 1.7*threshold)

    return summarized_text