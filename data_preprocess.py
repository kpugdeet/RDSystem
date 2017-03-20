from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import wordpunct_tokenize as wordpunct_tokenize
import re
import string
import numpy
import os
from cloudpickle import dump
from cloudpickle import load

PARAMS_DATA_PATH = os.path.dirname(os.path.abspath(__file__)) + "/data/RBMTopic/params/"

class DataPreprocess:

    #self-defined stop words list
    @staticmethod
    def get_stopwords():
        return [u'i', u'me', u'my', u'myself', u'we', u'our', u'ours', u'ourselves', u'you', u'your', u'yours',
                u'yourself',
                u'yourselves', u'he', u'him', u'his', u'himself', u'she', u'her', u'hers', u'herself', u'it', u'its',
                u'itself',
                u'they', u'them', u'their', u'theirs', u'themselves', u'what', u'which', u'who', u'whom', u'this',
                u'that',
                u'these',
                u'those', u'am', u'is', u'are', u'was', u'were', u'be', u'been', u'being', u'have', u'has', u'had',
                u'having', u'do',
                u'does', u'did', u'doing', u'a', u'an', u'the', u'and', u'but', u'if', u'or', u'because', u'as',
                u'until',
                u'while',
                u'of', u'at', u'by', u'for', u'with', u'about', u'against', u'between', u'into', u'through', u'during',
                u'before',
                u'after', u'above', u'below', u'to', u'from', u'up', u'down', u'in', u'out', u'on', u'off', u'over',
                u'under',
                u'again', u'further', u'then', u'once', u'here', u'there', u'when', u'where', u'why', u'how', u'all',
                u'any', u'both',
                u'each', u'few', u'more', u'most', u'other', u'some', u'such', u'no', u'nor', u'not', u'only', u'own',
                u'same', u'so',
                u'than', u'too', u'very', u's', u't', u'can', u'will', u'just', u'don', u'should', u'now']

    @staticmethod
    def stemmed_words(d):
        stemmer = PorterStemmer()
        attribute_names = [stemmer.stem(token.lower()) for token in wordpunct_tokenize(
            re.sub('[%s]' % re.escape(string.punctuation), '', d)) if
                           token.lower() not in DataPreprocess.get_stopwords()]
        return attribute_names

    def get_bag_words_matirx(self, data, max_vocaulary=None):
        self.vectorizer = CountVectorizer(tokenizer=DataPreprocess.stemmed_words, max_features=max_vocaulary)
        train_data = self.vectorizer.fit_transform(data)
        train_data_matrix = numpy.array(train_data.toarray())
        filename=PARAMS_DATA_PATH+"vocabulary.dat"
        with open(filename, "wb") as file:
           dump(self.vectorizer, file)
        return train_data_matrix

    def get_bag_words_matrix_by_vocabulary(self, data):
        filename = PARAMS_DATA_PATH + "vocabulary.dat"
        try:
            self.vectorizer=load(open(filename,"rb"))
        except:
            print("Cann't find vocuabluary!!!")
        new_data =self.vectorizer.transform(data)
        new_data_matrix = numpy.array(new_data.toarray())
        return new_data_matrix

