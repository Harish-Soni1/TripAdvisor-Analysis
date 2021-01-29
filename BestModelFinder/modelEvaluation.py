from sklearn.metrics import accuracy_score,confusion_matrix,precision_score,recall_score,f1_score

class ModelEvaluation:

    def __init__(self, trained_model, testX, testY, file_object, logger_object):
        self.trained_model = trained_model
        self.testX = testX
        self.testY = testY
        self.logger_object = logger_object
        self.file_object = file_object
        self.modelEvaluationDict = {
            'nb': {'accuracy_score': None, 'confusion_matrix': None, 'precision_score': None, 'recall_score': None,
                   'f1_score': None},
            'rf': {'accuracy_score': None, 'confusion_matrix': None, 'precision_score': None, 'recall_score': None,
                   'f1_score': None},
            'xg': {'accuracy_score': None, 'confusion_matrix': None, 'precision_score': None, 'recall_score': None,
                   'f1_score': None},
            'bnb': {'accuracy_score': None, 'confusion_matrix': None, 'precision_score': None, 'recall_score': None,
                    'f1_score': None}
        }


    def getAccuracyScore(self,model):
        file = open('TrainingLogs/GeneralLog.txt', 'a+')
        self.logger_object.log(file,'Entered getAccuracyScore method for '+ str(model) + ' of ModelTuner class')
        file.close()

        try:
            y_predict = model.predict(self.testX)
            acc_score = accuracy_score(self.testY,y_predict)
            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,'Successfully Executed getAccuracyScore for' +str(model)+ ' method of Model_Tuner class ')
            file.close()
            return acc_score
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception Occured in get_accuracy_score for ' + str(model) + ' ::%s' % str(e))
            self.logger_object.log(self.file_object, 'getAccuracyScore method .Exited !!')
            raise e

    def getConfusionMatrix(self, model):
        file = open('TrainingLogs/GeneralLog.txt', 'a+')
        self.logger_object.log(file, 'Entered getConfusionMatrix method for ' + str(model) + ' of Model_Finder class ')
        file.close()

        try:
            y_predict = model.predict(self.testX)
            cfn_matrix = confusion_matrix(self.testY, y_predict)
            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file, 'Successfully Executed getConfusionMatrix for' + str(
                model) + ' method of ModelFinder class ')
            file.close()
            return cfn_matrix
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception Occured in getConfusionMatrix for ' + str(model) + ' ::%s' % str(e))
            self.logger_object.log(self.file_object, 'getConfusionMatrix method .Exited !!')
            raise e

    def getPrecisionScore(self,model):
        file = open('TrainingLogs/GeneralLog.txt', 'a+')
        self.logger_object.log(file,'Entered getPrecisionScore method for '+ str(model) + ' of Model_Finder class ')
        file.close()

        try:
            y_predict = model.predict(self.testX)
            prec_score = precision_score(self.testY,y_predict)
            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,'Successfully Executed getPrecisionScore for ' +str(model)+ ' method of Model_Tuner class ')
            file.close()
            return prec_score
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception Occured in get_precision_score for ' + str(model) + ' ::%s' % str(e))
            self.logger_object.log(self.file_object, 'getPrecisionScore method .Exited !!')
            raise e

    def getRecallScore(self,model):
        file = open('TrainingLogs/GeneralLog.txt', 'a+')
        self.logger_object.log(file,'Entered getRecallScore method for '+ str(model) + ' of Model_Finder class ')
        file.close()

        try:
            y_predict = model.predict(self.testX)
            reca_score = recall_score(self.testY,y_predict)
            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,'Successfully Executed get_recall_score for ' +str(model)+ ' method of Model_Finder class ')
            file.close()
            return reca_score
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception Occured in get_recall_score for ' + str(model) + ' ::%s' % str(e))
            self.logger_object.log(self.file_object, 'getRecallScore method .Exited !!')
            raise e

    def getF1Score(self,model):
        file = open('TrainingLogs/GeneralLog.txt', 'a+')
        self.logger_object.log(file,'Entered getF1Score method for '+ str(model) + ' of Model_Finder class ')
        file.close()

        try:
            y_predict = model.predict(self.testX)
            f1_sc = f1_score(self.testY,y_predict)
            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,'Successfully Executed get_f1_score for ' +str(model)+ ' method of Model_Finder class ')
            file.close()
            return f1_sc
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception Occured in get_f1_score for ' + str(model) + ' ::%s' % str(e))
            self.logger_object.log(self.file_object, 'getF1Score method .Exited !!')
            raise e

    def generateModelsEvaluationReportDict(self,trained_models_dict):
        file = open('TrainingLogs/GeneralLog.txt', 'a+')
        self.logger_object.log(file, 'Entered generateModelsEvaluationReportDict method of Model_Evaluation class of model_evaluation package')
        file.close()

        try:
            for model,object in zip(trained_models_dict.keys(),trained_models_dict.values()):
                if object is not None:
                    self.modelEvaluationDict[model]['accuracy_score'] = self.getAccuracyScore(object)
                    self.modelEvaluationDict[model]['confusion_matrix'] = self.getConfusionMatrix(object)
                    self.modelEvaluationDict[model]['precision_score'] = self.getPrecisionScore(object)
                    self.modelEvaluationDict[model]['f1_score'] = self.getF1Score(object)

            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file, 'Successfully Executed generate_model_evaluation_report_dict() for method of Model_Evaluation class of model_evaluation package')
            file.close()

            self.logger_object.log(self.file_object,'Model Evaluation Report is :: %s' %str(self.modelEvaluationDict))
            return self.modelEvaluationDict
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception Occured in generate_model_evaluation_report_dict() ')
            self.logger_object.log(self.file_object, 'getF1Score method .Exited !!')
            raise e


