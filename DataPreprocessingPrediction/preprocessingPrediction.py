import pandas as pd
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import numpy as np
import re
from FileOperations import fileMethods


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
                self.usefullData = self.data.drop(labels=self.column, axis=1)
                file = open('PredictionLogs/GeneralLog.txt', 'a+')
                self.logger_object.log(file,
                    'Column Removal Succesfull. Exited to the removeColumn of the Preprocessor class')
                file.close()

            return self.usefullData
        except Exception as e:
            self.logger_object.log(self.file_object,
                'Exception occured in removeColumns method of the Preprocessor class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                'Column removal Unsuccessful. Exited the removeColumns method of the Preprocessor class')
            raise e

    def cleanReview(self, data):

        self.logger_object.log(self.file_object,
            'Entered in the cleanReviews of the Preproseccor class')

        self.data = data
        try:
            self.data["Comments"] = self.data["Comments"].apply(lambda x: cleanReviews(x))

            file = open('PredictionLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,
                'Review Cleaning Seuccesfull. Exited to the cleanReview of the Preprocessor class')
            file.close()

            return self.data
        except Exception as e:
            self.logger_object.log(self.file_object,
                'Exception occured in cleanReview method of the Preprocessor class. Exception message:  ' + str(
                                       e))
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
                           "wouldn", "wouldn't", "should", "should've", "no", "nor", "not", "very", "hotel",
                           "singapore"]

            for word in self.stopWords:
                if word in self.wanted:
                    self.stopWords.remove(word)

            self.data["Comments"] = self.data["Comments"].apply(
                lambda x: " ".join(x for x in x.split() if x not in self.stopWords))

            file = open('PredictionLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,
                'Remove StopWords Succesfull. Exited to the removeStopWords of the Preprocessor class')
            file.close()

            return self.data

        except Exception as e:
            self.logger_object.log(self.file_object,
                'Exception occured in removeStopWords method of the Preprocessor class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                'Remove StopWords Unsuccessful. Exited the removeStopWords method of the Preprocessor class')
            raise e

    def VectorizeText(self, data):

        self.logger_object.log(self.file_object,
            'Entered in the Lemmatizer of the Preprocessor class')

        self.data = data

        try:
            fileOperation = fileMethods.FileOperations(self.file_object, self.logger_object)
            vect = fileOperation.loadModel('Vectorizer')
            self.data = vect.transform(self.data['Comments'])

            tfidf = fileOperation.loadModel('TFIDFTransformer')
            self.data = tfidf.transform(self.data)
            self.data = self.data.toarray()

            file = open('PredictionLogs/General_Log.txt', 'a+')
            self.logger_object.log(file,
                'Successfully Executed count_vectorizer() method of PreProcessor_Prediction class of data_preprocessing package')

            return self.data
        except Exception as e:
            self.logger_object.log(self.file_object,
                'Exception occured in Lemmetizer method of the Preprocessor class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                'Lemmatization Unsuccessful. Exited the Lemmetizer method of the Preprocessor class')
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

                file = open('PredictionLogs/GeneralLog.txt', 'a+')
                self.logger_object.log(file,
                    'Finding Missing Succesfull. Exited to the isNullPresent of the Preprocessor class')
                file.close()

                return self.isNull
            else:
                self.logger_object.log(self.file_object,
                    'No Null Values Present. Exited to the isNullPresent of the Preprocessor class')
        except Exception as e:
            self.logger_object.log(self.file_object,
                'Exception occured in isNullPresent method of the Preprocessor class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                'Finding Missing Unsuccesfull. Exited to the isNullPresent of the Preprocessor class')
            raise e


def cleanReviews(s):
    s = s.lower()
    s = re.sub(r'[^\w\s]', ' ', s)
    s = re.sub(r'[\d+]', ' ', s)
    s = s.strip()
    s = re.sub(' +', ' ', s)
    return s
