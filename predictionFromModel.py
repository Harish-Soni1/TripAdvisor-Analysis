import pandas as pd
from DataPreprocessingPrediction import preprocessingPrediction
from DataTransformPrediction.dataTransformationPrediction import dataTransformPredict
from ApplicationLogging import logger
from FileOperations import fileMethods
from DataIngestion import dataLoaderPrediction
from datetime import datetime

class PredictionFromModel:

    def __init__(self):
        self.logger_object = logger.AppLogger()
        self.file_object = open('PredictionLogs/ModelPredictionLog.txt', 'a+')

    def predictData(self, file):

        logfile = open('PredictionLogs/GeneralLog.txt', 'a+')
        self.logger_object.log(logfile, 'Entered trainModel method of PredictionModel class')
        logfile.close()
        dataGetter = dataLoaderPrediction.DataGetterPred(self.file_object, self.logger_object)
        try:
            data = dataGetter.getData(file)
            print(data.columns)
            raw_data = data.copy(deep=True)
            preprocessor = preprocessingPrediction.Preprocessor(self.file_object, self.logger_object)

            data = preprocessor.cleanReview(data)
            data = preprocessor.removeStopWords(data)
            data = preprocessor.VectorizeText(data)

            fileOperation = fileMethods.FileOperations(self.file_object, self.logger_object)
            model = fileOperation.loadModel()
            prediction = list(model.predict(data))
            polar_label = pd.Series(find_polar_prediction(prediction), name='label')
            data_with_label = pd.concat([raw_data, polar_label], axis=1)
            fileName = "Prediction" + "_" + str(int(datetime.timestamp(datetime.now()))) + ".csv"
            data_with_label.to_csv('PredictedFiles/' + fileName, header=True, mode='a+')
            self.logger_object.log(self.file_object, 'Successfull End of Prediction !!!')

            return 1
        except Exception as e:
            self.logger_object.log(self.file_object, 'Unsuccessfull End of Prediction')
            self.file_object.close()
            raise e

def find_polar_prediction(pred_list):
    polar = list()
    for i in pred_list:
        if i == 2:
            polar.append('Positive')
        elif i == 1:
            polar.append('Neutral')
        elif i == 0:
            polar.append('Negative')
    return polar