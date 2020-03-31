# =============================================================================
# This class provides some tools for text preprocessing
# =============================================================================

import spacy
import re

class TextTools:
    def __init__(self):
        self.nlp = spacy.load('en')
        
    def __tokenize(self, text):
        return self.nlp(text)

    def __lemmatize(self, token_list):
        return [t.lemma_ for t in token_list]
    
    def __remove_stop_words(self, token_list):
        return [t for t in token_list if not t.is_stop]
    
    # This method removes all the characters that aren't latin letters or spaces 
    def __clean_str(self, text):
        return re.sub('[^a-zA-Z ]*', '', text)
    
    # This method calls __clean_str(..) on either a string or a list provided in input
    def clean(self, x): #string or list
        if isinstance(x, str):
            return self.__clean_str(x)
        else:
            return [self.__clean_str(item) for item in x if isinstance(item, str)]
    
    # This method cleans the text from special characters and numbers, tokenizes the text, removes english stop words and performs a lemmatization
    def preprocess(self, text) -> str:
        if not isinstance(text, str):
            return ''
        return ' '.join(self.__lemmatize(self.__remove_stop_words(self.__tokenize(self.__clean_str(text)))))