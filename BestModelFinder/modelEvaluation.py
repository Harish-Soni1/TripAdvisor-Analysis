from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score, classification_report
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import os


class ModelEvaluation:

    def __init__(self, trained_model, testX, testY, file_object, logger_object):
        self.trained_model = trained_model
        self.testX = testX
        self.testY = testY
        self.logger_object = logger_object
        self.file_object = file_object
        self.modelEvaluationDict = {
            'svm': {'AccuracyScore': None, 'ConfusionMatrix': None, 'PrecisionScore': None, 'RecallScore': None,
                   'F1Score': 0, 'ClassificationReport': None},
            'rf': {'AccuracyScore': None, 'ConfusionMatrix': None, 'PrecisionScore': None, 'RecallScore': None,
                   'F1Score': 0, 'ClassificationReport': None},
            'xg': {'AccuracyScore': None, 'ConfusionMatrix': None, 'PrecisionScore': None, 'RecallScore': None,
                   'F1Score': 0, 'ClassificationReport': None},
            'bnb': {'AccuracyScore': None, 'ConfusionMatrix': None, 'PrecisionScore': None, 'RecallScore': None,
                    'F1Score': 0, 'ClassificationReport': None}
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
            self.logger_object.log(self.file_object,'Exception Occured in getAccuracyScore for ' + str(model) + ' ::%s' % str(e))
            self.logger_object.log(self.file_object, 'getAccuracyScore method .Exited !!')
            raise e

    def getConfusionMatrix(self, model):
        file = open('TrainingLogs/GeneralLog.txt', 'a+')
        self.logger_object.log(file, 'Entered getConfusionMatrix method for ' + str(model) + ' of ModelFinder class ')
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
        self.logger_object.log(file,'Entered getPrecisionScore method for '+ str(model) + ' of ModelFinder class ')
        file.close()

        try:
            y_predict = model.predict(self.testX)
            prec_score = precision_score(self.testY,y_predict, average='macro')
            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,'Successfully Executed getPrecisionScore for ' +str(model)+ ' method of Model_Tuner class ')
            file.close()
            return prec_score
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception Occured in getPrecisionScore for ' + str(model) + ' ::%s' % str(e))
            self.logger_object.log(self.file_object, 'getPrecisionScore method .Exited !!')
            raise e

    def getRecallScore(self,model):
        file = open('TrainingLogs/GeneralLog.txt', 'a+')
        self.logger_object.log(file,'Entered getRecallScore method for '+ str(model) + ' of ModelFinder class ')
        file.close()

        try:
            y_predict = model.predict(self.testX)
            reca_score = recall_score(self.testY,y_predict, average='macro')
            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,'Successfully Executed getRecallScore for ' +str(model)+ ' method of ModelFinder class ')
            file.close()
            return reca_score
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception Occured in getRecallScore for ' + str(model) + ' ::%s' % str(e))
            self.logger_object.log(self.file_object, 'getRecallScore method .Exited !!')
            raise e

    def getF1Score(self,model):
        file = open('TrainingLogs/GeneralLog.txt', 'a+')
        self.logger_object.log(file,'Entered getF1Score method for '+ str(model) + ' of ModelFinder class ')
        file.close()

        try:
            y_predict = model.predict(self.testX)
            f1_sc = f1_score(self.testY,y_predict, average='macro')
            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,'Successfully Executed getF1Score for ' +str(model)+ ' method of ModelFinder class ')
            file.close()
            return f1_sc
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception Occured in getF1Score for ' + str(model) + ' ::%s' % str(e))
            self.logger_object.log(self.file_object, 'getF1Score method .Exited !!')
            raise e

    def getClassificationReport(self, model):
        file = open('TrainingLogs/GeneralLog.txt', 'a+')
        self.logger_object.log(file, 'Entered getClassificationReport method for ' + str(model) + ' of ModelFinder class ')
        file.close()
        try:
            y_preict = model.predict(self.testX)
            clsReport = classification_report(self.testY, y_preict, output_dict=True)
            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file, 'Successfully Executed getClassificationReport for ' + str(
                model) + ' method of ModelFinder class ')
            file.close()
            return clsReport
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception Occured in getClassificationReport for ' + str(model) + ' ::%s' % str(e))
            self.logger_object.log(self.file_object, 'getClassificationReport method .Exited !!')
            raise e

    def generateModelsEvaluationReportDict(self,trained_models_dict):
        file = open('TrainingLogs/GeneralLog.txt', 'a+')
        self.logger_object.log(file, 'Entered generateModelsEvaluationReportDict method of Model_Evaluation class of model_evaluation package')
        file.close()

        try:
            for model,object in zip(trained_models_dict.keys(),trained_models_dict.values()):
                if object is not None:
                    self.modelEvaluationDict[model]['AccuracyScore'] = self.getAccuracyScore(object)
                    self.modelEvaluationDict[model]['ConfusionMatrix'] = self.getConfusionMatrix(object)
                    self.modelEvaluationDict[model]['PrecisionScore'] = self.getPrecisionScore(object)
                    self.modelEvaluationDict[model]['RecallScore'] = self.getRecallScore(object)
                    self.modelEvaluationDict[model]['F1Score'] = self.getF1Score(object)
                    self.modelEvaluationDict[model]['ClassificationReport'] = self.getClassificationReport(object)
                    self.generateImage(self.getConfusionMatrix(object), model)

            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file, 'Successfully Executed generateModelsEvaluationReportDict for method of Model_Evaluation class of model_evaluation package')
            file.close()

            self.logger_object.log(self.file_object,'Model Evaluation Report is :: %s' %str(self.modelEvaluationDict))
            return self.modelEvaluationDict
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception Occured in generateModelsEvaluationReportDict ')
            self.logger_object.log(self.file_object, 'generateModelsEvaluationReportDict method .Exited !!')
            raise e

    def generateImage(self, matrix, model):
        file = open('TrainingLogs/GeneralLog.txt', 'a+')
        self.logger_object.log(file,
            'Entered generateImage method of Model_Evaluation class of model_evaluation package')
        file.close()
        try:
            classes = ["0", "1", "2"]
            df_cfm = pd.DataFrame(matrix, index=classes, columns=classes)
            plt.figure(figsize=(10, 10))
            cfm_plot = sn.heatmap(df_cfm, annot=True, fmt='g')
            fileName = model + "_" + "confusion_matrix.png"
            path = os.path.join("Documents/" + fileName)
            cfm_plot.figure.savefig(path)

        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception Occured in generateImage() ')
            self.logger_object.log(self.file_object, 'generateImage method .Exited !!')
            raise e
