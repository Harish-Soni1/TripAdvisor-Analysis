from sklearn.model_selection import train_test_split
from DataIngestion import dataLoader
from DataPreprocessing import preprocessing
from BestModelFinder import tuner
from FileOperations import fileMethods
from DataTransform.dataTransformation import dataTransform 
from ApplicationLogging import logger
from BestModelFinder import modelEvaluation, PDFCreation

class TrainingModel:

    def __init__(self, modelsList, samplingMethod,):
        self.logger_object = logger.AppLogger()
        self.file_object = open('TrainingLogs/ModelTrainingLog.txt','a+')
        self.samplingMethod = samplingMethod
        self.modelsList = modelsList

    def trainModel(self):
        file = open('TrainingLogs/GeneralLog.txt', 'a+')
        self.logger_object.log(file,'Entered trainModel method of TrainingModel class')
        file.close()

        try:
            dataGetter = dataLoader.DataGetter(self.file_object, self.logger_object)
            data = dataGetter.getData()
            preprocessor = preprocessing.Preprocessor(self.file_object, self.logger_object)

            X, Y = preprocessor.separateLabelFeatures(data, labelCoulmnName='Ratings')
            isNullPresent = preprocessor.isNullPresent(X)

            if(isNullPresent):
                X = dataTransform.replaceMissingValueWithNull(X)

            X = preprocessor.cleanReview(X)
            X = preprocessor.removeStopWords(X)
            X = preprocessor.Lemmatizer(X)
            Y = preprocessor.polarizeRating(Y)

            x_train,x_test,y_train,y_test = train_test_split(X, Y, test_size=0.3, random_state=100)
            x_train,x_test, vect, tfidf = preprocessor.vectorizeText(x_train, x_test)

            if self.samplingMethod == 'us':
                x_train,y_train = preprocessor.underSampling(x_train, y_train)

            elif self.samplingMethod == 'os':
                x_train, y_train = preprocessor.overSampling(x_train, y_train)

            else:
                pass

            modelFinder = tuner.ModelFinder(self.file_object, self.logger_object)
            self.trainedModelsDict = {'svm':None, 'rf':None, 'xg':None, 'bnb':None}

            for m in self.modelsList:
                if m == 'svm':
                    self.trainedModelsDict['svm'] = modelFinder.bestParaMeterForSupportVector(x_train,y_train)

                elif m == 'rf':
                    self.trainedModelsDict['rf'] = modelFinder.getBestParamsForRandomForest(x_train,y_train)

                elif m == 'xg':
                    self.trainedModelsDict['xg'] = modelFinder.bestOnvsRestClassifierModel(x_train,y_train)

                elif m == 'bnb':
                    self.trainedModelsDict['bnb'] = modelFinder.getBestBaggingClassifier(x_train,y_train)

                else:
                    pass
            
            modelEvaluate = modelEvaluation.ModelEvaluation(self.trainedModelsDict, x_test, y_test, self.file_object, self.logger_object)
            pdf = PDFCreation.PDF(self.file_object, self.logger_object)
            self.modelEvaluationReportDict =  modelEvaluate.generateModelsEvaluationReportDict(self.trainedModelsDict)
            self.orderedModelEvaluationReportDict = sorted(self.modelEvaluationReportDict.items(),key=lambda x:x[1]['F1Score'],reverse=True)
            pdf.generatePDF(self.orderedModelEvaluationReportDict)

            for model in self.orderedModelEvaluationReportDict:
                model_to_save = model
                break

            fileOperation = fileMethods.FileOperations(self.file_object,self.logger_object)
            isModelSaved = fileOperation.saveModel(self.trainedModelsDict[model_to_save[0]], model_to_save[0])
            fileOperation.saveModel(vect, "Vectorizer")
            fileOperation.saveModel(tfidf, "TFIDFTransformer")

            if (isModelSaved == 'success'):
                self.logger_object.log(self.file_object, 'Successfull End of Training')
            else:
                self.logger_object.log(self.file_object, 'Error while saving model to models directory')

        except Exception as e:
            self.logger_object.log(self.file_object, 'Unsuccessfull End of Training')
            self.file_object.close()
            raise e
