import re
import contractions
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import gensim.downloader
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
# glove-twitter-25
# w2v_model = gensim.downloader.load('word2vec-google-news-300')

# The tow are loaded slowly, use as global
w2v_model = gensim.downloader.load('glove-twitter-25')
lemmatizer = WordNetLemmatizer()


def data_preprocessing(sentence):
    global lemmatizer
    sentence = re.sub('<[^<]+?>', ' ', sentence)                        # noise removal
    sentence = contractions.fix(sentence)                               # Expand contractions
    sentence = " ".join(item.lower() for item in sentence.split())      # convert to lower case
    sentence = nltk.word_tokenize(sentence)                             # tokenization
    sentence = " ".join(item for item in sentence if item not in stopwords.words("english"))    # remove stopwords
    sentence = " ".join([lemmatizer.lemmatize(word) for word in sentence.split()])              # Lemmatization

    return sentence


def generate_w2v_feature(sentence, feature_size=25):
    global w2v_model
    return np.mean([w2v_model[w] for w in nltk.word_tokenize(sentence) if w in w2v_model]
                   or [np.zeros(feature_size)], axis=0)
