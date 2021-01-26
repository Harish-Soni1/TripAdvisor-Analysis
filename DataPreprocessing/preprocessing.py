import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk import FreqDist
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.util import ngrams
from nltk.corpus import stopwords, wordnet
import numpy as np
import re

class Preprocessor:

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.vect = CountVectorizer()
        self.tfidf = TfidfTransformer()

    def removeColumns(self, data, columns):

        self.logger_object.log(self.file_object,
            'Entered in the removeColumn of the Preprocessor class')

        self.data = data
        self.columns = columns[0]

        try:

            if self.columns in self.data.columns:
                self.usefullData = self.data.drop(labels = self.columns, axis = 1)
                self.logger_object.log(self.file_object, 
                    'Column Removal Succesfull. Exited to the removeColumn of the Preprocessor class')    
            
            return self.usefullData
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in removeColumns method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,
                'Column removal Unsuccessful. Exited the removeColumns method of the Preprocessor class')
            raise Exception()

    def cleanReview(self, data):

        self.logger_object.log(self.file_object,
            'Entered in the cleanReviews of the Preproseccor class')
        
        self.data = data
        try:
            self.data = self.data.lower()
            self.data = re.sub(r'[^\w\s]', ' ', self.data)
            self.data = re.sub(r'[\d+]', ' ', self.data)    
            self.data = self.data.strip()                   
            self.data = re.sub(' +', ' ', self.data)        
            
            self.logger_object.log(self.file_object,
                'Review Cleaning Seuccesfull. Exited to the cleanReview of the Preprocessor class')

            return self.data
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in cleanReview method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,
                'Review Cleaning Unsuccessful. Exited the cleanReview method of the Preprocessor class')
            raise Exception()

    def removeStopWords(self, data):

        self.logger_object.log(self.file_object, 
            'Entered in the removeStopWords of the Preprocessor class')

        self.data = data
        self.stopWords = stopwords.words('english')
        try:
            self.wanted = ["ain", "aren", "aren't", "couldn", "couldn't", 
                "didn", "didn't", "doesn", "doesn't", "hadn", "hadn't", "hasn", 
                "hasn't", "haven", "haven't", "isn", "isn't", "mightn", "mightn't", 
                "mustn", "mustn't", "needn", "needn't", "shan", "shan't", "shouldn", 
                "shouldn't", "won", "wasn", "wasn't", "weren", "weren't", "won't", 
                "wouldn", "wouldn't", "should", "should've", "no", "nor", "not", "very"]
            
            for word in self.stopWords:
                if word in self.wanted:
                    self.stopWords.remove(word)
            
            self.newData = self.data.apply(lambda x: " ".join(x for x in x.split() if x not in stop_words))
            self.logger_object.log(self.file_object,
                'Remove StopWords Succesfull. Exited to the removeStopWords of the Preprocessor class')

            return self.newData

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in removeStopWords method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,
                'Remove StopWords Unsuccessful. Exited the removeStopWords method of the Preprocessor class')
            raise Exception()

    def Lemmatizer(self, data):

        self.logger_object.log(self.file_object, 
            'Entered in the Lemmatizer of the Preprocessor class')

        self.data = data

        try:
            self.newData = self.data.apply(lambda x: lemmatizeText(x))
            self.finalData = self.newData.apply(lambda x: stringifyData(x))

            self.logger_object.log(self.file_object,
                'Lemmatization Succesfull. Exited to the Lemmetizer of the Preprocessor class')

            return self.finalData
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in Lemmetizer method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,
                'Lemmatization Unsuccessful. Exited the Lemmetizer method of the Preprocessor class')
            raise Exception()

    def polarizeRating(self, rate):

        self.logger_object.log(self.file_object, 
            'Entered in the polarizeRating of the Preprocessor class')

        self.rate = rate
        try:
            self.polarizeRate = self.rate.apply(lambda x: 'Positive' if x > 3 else('Neutral' if x==3 else 'Negative'))
            self.logger_object.log(self.file_object,
                'Polarizing Succesfull. Exited to the prolarizeRating of the Preprocessor class')

            return self.polarizeRate
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in prolarizeRating method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,
                'Polarizing Unsuccessful. Exited the prolarizeRating method of the Preprocessor class')
            raise Exception()

    def separateLabelFeatures(self, data, labelCoulmnName):

        self.logger_object.log(self.file_object,
            'Entered in the separateLabelFeatures of the Preprocessor class')

        try:
            self.X = data.drop(labels = labelCoulmnName, axis = 1)
            self.Y = data[labelCoulmnName]

            self.logger_object.log(self.file_object, 
                'Separation Succesfull. Exited to the separateLabelFeatures of the Preprocessor class')

            return self.X, self.Y
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in separateLabelFeatures method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,
                'Separation Unsuccessful. Exited the separateLabelFeatures method of the Preprocessor class')
            raise Exception()

    def isNullPresent(self, data):

        self.logger_object.log(self.file_object,
            'Entered in the isNullPresent of the Preprocessor class')

        self.data = data
        self.isNull = False
        try:
            self.nullCount = data.isna().sum()
            
            for i in self.nullCount:
                if i > 0:
                    self.isNull = True

            if self.isNull:
                dataFrameWithNull = pd.DataFrame()
                dataFrameWithNull['columns'] = data.columns
                dataFrameWithNull['missingValueCount'] = np.asarray(data.isna().sum())
                dataFrameWithNull.to_csv('preprocessing_data/null_values.csv')

                self.logger_object.log(self.file_object, 
                    'Finding Missing Succesfull. Exited to the isNullPresent of the Preprocessor class')
                
                return self.isNull
            else:
                self.logger_object.log(self.file_object, 
                    'No Null Values Present. Exited to the isNullPresent of the Preprocessor class')
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in isNullPresent method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,
                'Finding Missing Unsuccesfull. Exited to the isNullPresent of the Preprocessor class')
            raise Exception()

    def vectorizeText(self, trainX, testX):
        self.logger_object.log(self.file_object,
            'Entered in the vectorizeText of the Preprocessor class')
        
        self.trainX = trainX
        self.testX = testX

        try:
            self.trainX = self.vect.fit_transform(self.trainX)
            self.testX = self.vect.transform(self.testX)

            self.trainX = self.tfidf.fit_transform(self.trainX)
            self.testX = self.tfidf.transform(self.testX)
            self.trainX = self.trainX.toarray()
            self.testX = self.testX.toarray()

            self.logger_object.log(self.file_object,
                'Vectorize Text Succesfull. Exited to the vectorizeText of the Preprocessor class')
            return self.trainX, self.testX

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in vectorizeText method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,
                'Vectorize Text Unsuccesfull. Exited to the isNullPresent of the Preprocessor class')
        raise Exception()
        

def toWordNet(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:          
        return None

def lemmatizeText(text):
    lemm = WordNetLemmatizer()
    nltk_tagged = nltk.pos_tag(text)
    wordnet_tagged = map(lambda x: (x[0], toWordNet(x[1])), nltk_tagged)
    lemm_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None:
            lemm_sentence.append(word)
        else:
            lemm_sentence.append(lemm.lemmatize(word, tag))
    return lemm_sentence


def stringifyData(text):
    return ' '.join(str(elem) for elem in text)