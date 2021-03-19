import re
import string
import math 

class Similarity(object):

    def __init__(self, stop_words=True):
        self.stop_words = stop_words

    def tokenize(self, text):
        """Tokenize the given text and optionally to remove stop words

        Args:
            text (str)

        Returns:
            tokens (list)
        """
        tokens = re.findall(r"\w+", text)
        stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 
        'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 
        'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 
        'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 
        'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 
        'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 
        'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 
        'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 
        'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 
        'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 
        'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 
        'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 
        'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 
        'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 
        'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 
        're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', 
        "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven',
        "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 
        'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 
        'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", 'film', 'films']
        if self.stop_words:
            tokens = [token for token in tokens if token not in stop_words]
        return tokens

    def get_all_chars(self, text_list):
        """Get a dict of tokens that contains all characters for all texts

        Args:
            text_list ([list]): A list of raw texts

        Returns:
            set
        """
        tokenized_texts = [self.tokenize(text) for text in text_list]
        all_chars = set().union(*tokenized_texts)
        return all_chars

    def get_word_frequency(self, words, all_chars):
        """Get the word frequency for a tokenized text

        Args:
            words (list): a list of tokens for a text
            all_chars (set): a set of unique tokens for all texts

        Returns:
            dict: the word frequency for a text
        """
        word_dict = dict.fromkeys(all_chars, 0)
        for word in words:
            word_dict[word] += 1
        return word_dict

    def compute_tf(self, word_dict, words):
        """Get the term frequency for a text

        Args:
            word_dict (dict): the word frequency for a text
            words (list): a list of tokens for a text

        Returns:
            dict
        """
        tf = {}
        for word, frequency in word_dict.items():
            tf[word] = frequency/float(len(words))
        return tf

    def compute_idf(self, doc_list):
        """Get the inverse document frequency for a text

        Args:
            doc_list (list): a list of word frequency dictionaries for two texts

        Returns:
            dict
        """
        idf = dict.fromkeys(doc_list[0].keys(), 0)
        for word, value in idf.items():
            doc_with_word_count =  sum([1 if doc[word] > 0 else 0 for i, doc in enumerate(doc_list)])
            idf[word] = math.log10((len(doc_list) + 1) / (float(doc_with_word_count) + 1) + 1)
        return idf

    def compute_tfidf(self, tf, idf):
        """Compute the term frequency and inverse dcoument frequency matrix

        Args:
            tf (dict): term frequency dictionary for a text
            idf (dict): inverse document frequency dictionary for all texts

        Returns:
            list: tf-idf matrix for a text
        """
        tfidf_dict = {}
        for word, value in tf.items():
            tfidf_dict[word] = value * idf[word]
        tfidf = list(tfidf_dict.values())
        return tfidf

    def compute_similarity(self, tfidf_a, tfidf_b):
        """Get the similarity score for two documents. Documents that are exactly 
        the same should get a score of 1, and documents that don’t have any words 
        in common should get a score of 0.

        Args:
            tfidf_a (list): tfidf matrix for first document
            tfidf_b (list): tfidf matrix for second document

        Returns:
            float: similiarity score
        """
        numerator = 0
        for i in range(len(tfidf_a)):
            numerator += tfidf_a[i] * tfidf_b[i]
        print(numerator)
        denominator = math.sqrt(sum([i ** 2 for i in tfidf_a])) * math.sqrt(sum([i ** 2 for i in tfidf_b]))
        print(denominator)
        similarity = round(numerator / denominator, 2)
        return similarity

    def get_result(self, text_a, text_b):
        """Compute the similarity score for two texts.Documents that are exactly 
        the same should get a score of 1, and documents that don’t have any words 
        in common should get a score of 0.

        Args:
            text_a (str): first text
            text_b (str): second text

        Returns:
            float: similiarity score
        """
        sample_a = self.tokenize(text_a)
        sample_b = self.tokenize(text_b)
        all_chars = self.get_all_chars([text_a, text_b])
        word_dict_a = self.get_word_frequency(sample_a, all_chars)
        word_dict_b = self.get_word_frequency(sample_b, all_chars)
        tf_a = self.compute_tf(word_dict_a, sample_a)
        tf_b = self.compute_tf(word_dict_b, sample_b)
        doc_list = [word_dict_a, word_dict_b]
        idf = self.compute_idf(doc_list)
        tfidf_a = self.compute_tfidf(tf_a, idf)
        tfidf_b = self.compute_tfidf(tf_b, idf)
        result = self.compute_similarity(tfidf_a, tfidf_b)
        return result