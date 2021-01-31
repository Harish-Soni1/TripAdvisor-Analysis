import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import NearMiss
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords, wordnet
import numpy as np
import re

class Preprocessor:

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.tokenizer = RegexpTokenizer(r'\w+')

    def removeColumns(self, data, columns):

        self.logger_object.log(self.file_object,
            'Entered in the removeColumn of the Preprocessor class')

        self.data = data
        self.column = columns[0]

        try:
            if self.column in self.data.columns:
                self.usefullData = self.data.drop(labels = self.column, axis = 1)
                file = open('TrainingLogs/GeneralLog.txt', 'a+')
                self.logger_object.log(file,
                    'Column Removal Succesfull. Exited to the removeColumn of the Preprocessor class')
                file.close()
            
            return self.usefullData
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in removeColumns method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,
                'Column removal Unsuccessful. Exited the removeColumns method of the Preprocessor class')
            raise e

    def cleanReview(self, data):

        self.logger_object.log(self.file_object,
            'Entered in the cleanReviews of the Preproseccor class')
        
        self.data = data
        try:
            self.data["Comments"] = self.data["Comments"].apply(lambda x: cleanReviews(x))

            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,
                'Review Cleaning Seuccesfull. Exited to the cleanReview of the Preprocessor class')
            file.close()

            return self.data
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in cleanReview method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,
                'Review Cleaning Unsuccessful. Exited the cleanReview method of the Preprocessor class')
            raise e

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
                "wouldn", "wouldn't", "should", "should've", "no", "nor", "not", "very", "hotel", "singapore"]
            
            for word in self.stopWords:
                if word in self.wanted:
                    self.stopWords.remove(word)
            
            self.data["Comments"] = self.data["Comments"].apply(lambda x: " ".join(x for x in x.split() if x not in self.stopWords))

            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,
                'Remove StopWords Succesfull. Exited to the removeStopWords of the Preprocessor class')
            file.close()

            return self.data

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in removeStopWords method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,
                'Remove StopWords Unsuccessful. Exited the removeStopWords method of the Preprocessor class')
            raise e

    def Lemmatizer(self, data):

        self.logger_object.log(self.file_object, 
            'Entered in the Lemmatizer of the Preprocessor class')

        self.data = data

        try:
            self.data["Comments"] = self.data["Comments"].apply(str)
            self.data["Comments"] = self.data["Comments"].apply(lambda x: self.tokenizer.tokenize(x))

            self.data["Comments"] = self.data["Comments"].apply(lambda x: lemmatizeText(x))
            self.data["Comments"] = self.data["Comments"].apply(lambda x: stringifyData(x))

            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,
                'Lemmatization Succesfull. Exited to the Lemmetizer of the Preprocessor class')
            file.close()

            return self.data
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in Lemmetizer method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,
                'Lemmatization Unsuccessful. Exited the Lemmetizer method of the Preprocessor class')
            raise e

    def polarizeRating(self, rate):

        self.logger_object.log(self.file_object, 
            'Entered in the polarizeRating of the Preprocessor class')

        self.rate = rate
        try:
            self.polarizeRate = self.rate.apply(lambda x: 2 if x > 3 else(1 if x==3 else 0))

            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,
                'Polarizing Succesfull. Exited to the prolarizeRating of the Preprocessor class')
            file.close()

            return self.polarizeRate
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in prolarizeRating method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,
                'Polarizing Unsuccessful. Exited the prolarizeRating method of the Preprocessor class')
            raise e

    def separateLabelFeatures(self, data, labelCoulmnName):

        self.logger_object.log(self.file_object,
            'Entered in the separateLabelFeatures of the Preprocessor class')

        try:
            self.X = data.drop(labels = labelCoulmnName, axis = 1)
            self.Y = data[labelCoulmnName]

            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,
                'Separation Succesfull. Exited to the separateLabelFeatures of the Preprocessor class')
            file.close()

            return self.X, self.Y
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in separateLabelFeatures method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,
                'Separation Unsuccessful. Exited the separateLabelFeatures method of the Preprocessor class')
            raise e

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

                file = open('TrainingLogs/GeneralLog.txt', 'a+')
                self.logger_object.log(file,
                    'Finding Missing Succesfull. Exited to the isNullPresent of the Preprocessor class')
                file.close()
                
                return self.isNull
            else:
                self.logger_object.log(self.file_object, 
                    'No Null Values Present. Exited to the isNullPresent of the Preprocessor class')
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in isNullPresent method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,
                'Finding Missing Unsuccesfull. Exited to the isNullPresent of the Preprocessor class')
            raise e

    def vectorizeText(self, trainX, testX):
        self.logger_object.log(self.file_object,
            'Entered in the vectorizeText of the Preprocessor class')
        
        self.trainX = trainX
        self.testX = testX

        try:
            vect = CountVectorizer()
            self.trainX = vect.fit_transform(self.trainX["Comments"])
            self.testX = vect.transform(self.testX["Comments"])

            tfidf = TfidfTransformer()
            self.trainX = tfidf.fit_transform(self.trainX)
            self.testX = tfidf.transform(self.testX)
            self.trainX = self.trainX.toarray()
            self.testX = self.testX.toarray()

            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,
                'Vectorize Text Succesfull. Exited to the vectorizeText of the Preprocessor class')
            file.close()

            return self.trainX, self.testX, vect, tfidf

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in vectorizeText method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,
                'Vectorize Text Unsuccesfull. Exited to the isNullPresent of the Preprocessor class')
            raise e
        
    def overSampling(self, trainX, trainY):
        self.logger_object.log(self.file_object,
            'Entered in the overSampling of the Preprocessor class')
        
        self.trainX = trainX
        self.trainY = trainY
        
        try:
            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,
                'trainX shape before over-sampling: ' + str(sum(self.trainY == 2)))
            self.logger_object.log(file,
                'trainX shape before over-sampling: ' + str(sum(self.trainY == 0)))
            self.logger_object.log(file,
                'trainX shape before over-sampling: ' + str(sum(self.trainY == 1)))

            self.overSample = SMOTE(random_state = 42, sampling_strategy = "auto")
            self.trainX, self.trainY = self.overSample.fit_sample(self.trainX, self.trainY)

            self.logger_object.log(file,
                'trainX shape after over-sampling: ' + str(sum(self.trainY == 2)))
            self.logger_object.log(file,
                'trainX shape after over-sampling: ' + str(sum(self.trainY == 0)))
            self.logger_object.log(file,
                'trainX shape after over-sampling: ' + str(sum(self.trainY == 1)))
            file.close()

            return self.trainX, self.trainY
        
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in overSampling method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,
                'Over Sampling of data Unsuccesfull. Exited to the overSampling of the Preprocessor class')
            raise e

    def underSampling(self, trainX, trainY):
        self.logger_object.log(self.file_object,
            'Entered in the underSampling of the Preprocessor class')

        self.trainX = trainX
        self.trainY = trainY
        try:
            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,
                'trainX shape before under-sampling: ' + str(sum(self.trainY == 2)))
            self.logger_object.log(file,
                'trainX shape before under-sampling: ' + str(sum(self.trainY == 0)))
            self.logger_object.log(file,
                'trainX shape before under-sampling: ' + str(sum(self.trainY == 1)))

            self.underSample = NearMiss(version = 1)
            self.trainX, self.trainY = self.underSample.fit_sample(self.trainX, self.trainY)

            self.logger_object.log(file,
                'trainX shape after under-sampling: ' + str(sum(self.trainY == 2)))
            self.logger_object.log(file,
                'trainX shape after under-sampling: ' + str(sum(self.trainY == 0)))
            self.logger_object.log(file,
                'trainX shape after under-sampling: ' + str(sum(self.trainY == 1)))
            file.close()

            return self.trainX, self.trainY
            
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in underSampling method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,
                'Under Sampling of data Unsuccesfull. Exited to the underSampling of the Preprocessor class')
            raise e


def cleanReviews(s):
    s = s.lower()
    s = re.sub(r'[^\w\s]', ' ', s)
    s = re.sub(r'[\d+]', ' ', s)
    s = s.strip()
    s = re.sub(' +', ' ', s)
    return s

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