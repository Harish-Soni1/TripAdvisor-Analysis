from sklearn.model_selection import train_test_split
from DataIngestion import dataLoader
from DataPreprocessing import preprocessing
from BestModelFinder import tuner
from FileOperations import fileMethods
from DataTransform.dataTransformation import dataTransform 
from ApplicationLogging import logger

class TrainModel:

    def __init__(self):
        self.log_writer = logger.AppLogger()
        self.file_object = open("Training_Logs/ModelTrainingLog.txt", 'a+')

    def trainingOfModel(self, modelName):
        self.log_writer.log(self.file_object, 'Start of Training')
        try:
            dataGetter = dataLoader.DataGetter(self.file_object, self.log_writer)
            data = dataGetter.getData()

            preProcessor = preprocessing.Preprocessor(self.file_object, self.log_writer)
            data = preProcessor.removeColumns(data, ['Unnamed: 0'])

            X, Y = preProcessor.separateLabelFeatures(data, labelCoulmnName='Ratings')
            isNullPresent = preProcessor.isNullPresent(X)

            if(isNullPresent):
                X = dataTransform.replaceMissingValueWithNull(X)

            X = preProcessor.cleanReview(X)
            X = preProcessor.removeStopWords(X)
            X = preProcessor.Lemmatizer(X)
            Y = preProcessor.polarizeRating(Y)

            x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state = 355)
            x_train, x_test = preProcessor.vectorizeText(x_train, x_test)
            modelFinder = tuner.ModelFinder(self.file_object, self.log_writer)
            bestModelName, bestModel = modelFinder.getBestModel(x_train, y_train, x_test, y_test, modelName)
           
            fileOp = fileMethods.FileOperations(self.file_object, self.logger_object)
            saveModel = fileOp.saveModel(bestModel, bestModelName)

            self.log_writer.log(self.file_object, 'Successful End of Training')
            self.file_object.close()
        
        except Exception as e:
            self.log_writer.log(self.file_object, 'Unsuccessful End of Training')
            self.file_object.close()
            raise e