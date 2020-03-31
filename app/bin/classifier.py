# This class provides some tools to classify text

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import ComplementNB
from sklearn.metrics import f1_score, plot_confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bin.text_tools import TextTools
import numpy as np

cosine = lambda x,y: np.dot(x, y) / (np.sqrt(np.dot(x,x)) * np.sqrt(np.dot(y,y)))

class Classifier:
    def __init__(self, max_df=0.80, max_features=6500):
        self.count_vect = TfidfVectorizer(max_df=max_df, stop_words='english', max_features=max_features, use_idf=True)
        self.cnb = ComplementNB()
        np.random.seed(2222)
        
    def __fit(self):
        self.cnb.fit(self.x_train, self.train_set['category'])

    # Calling this method just after object creation is required in order to set up data
    # Attribute test_size specifies the magnitude of the test set  
    def set_data(self, dataset:pd.DataFrame, labels:list, test_size=0.25):
        self.train_set, self.test_set = train_test_split(dataset, test_size=test_size)
        self.x_train = self.count_vect.fit_transform(self.train_set['text'])
        self.labels = labels
        self.__fit()

    # This method returns the predicted label for the text provided    
    def predict(self, text:str):
        txt = TextTools()
        text = txt.preprocess(text)
        feats = self.count_vect.transform([text])
        return self.cnb.predict(feats)
    
    # This method returns a matrix of probabilities computet by Complement Naive Bayes  
    def get_predict_proba(self, text:str):
        feats = self.count_vect.transform([text])
        predictions = {'label':(self.cnb.predict(feats))[0], 'features':self.cnb.predict_proba(feats)}
        return predictions

    # This method returns the f1-score 
    def get_score(self):
        x_test = self.count_vect.transform(self.test_set['text'])
        y_test_pred = self.cnb.predict(x_test)
        return f1_score(self.test_set['category'], y_test_pred, average=None, labels=self.labels).mean()

    # This method plots the confusion matrix
    def get_cmatrix(self):
        x_test = self.count_vect.transform(self.test_set['text'])
        y_test_pred = self.cnb.predict(x_test)
        disp = plot_confusion_matrix(self.cnb, x_test, self.test_set['category'], display_labels=self.labels, cmap=plt.cm.Blues, normalize='true')
        plt.show()

    # This method computes the cosine similarity between item1 and item2
    # item[1,2] must be array-like
    def similarity(self, item1, item2):
        return cosine(item1, item2)