from fpdf import FPDF
import os
import pandas as pd
import numpy as np


class PDF:

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.pdf = FPDF(format='A4', orientation='P')

    def generatePDF(self, dict):
        file = open('TrainingLogs/GeneralLog.txt', 'a+')
        self.logger_object.log(file,
            'Entered generatePDF method of PDF class')
        file.close()

        try:

            for data in dict:
                if data[1]['AccuracyScore'] is not None:

                    if data[0] == 'svm':
                        model = "Support Vector Machine Classifier"
                    elif data[0] == 'rf':
                        model = "Random Forest"
                    elif data[0] == 'xgb':
                        model = "XGBoost"
                    else:
                        model = "Bagging Classifier"

                    accuracyScore = data[1]['AccuracyScore']
                    precisionScore = data[1]['PrecisionScore']
                    recallScore = data[1]['RecallScore']
                    f1Score = data[1]['F1Score']
                    clsReport = data[1]['ClassificationReport']

                    newData = pd.DataFrame(clsReport)
                    newData = newData.transpose()
                    newData.drop(['accuracy', 'macro avg', 'weighted avg'], inplace=True)
                    newData['ratings'] = ['Negative', 'Neutral', 'Positive']
                    newData = newData[['ratings', 'precision', 'recall', 'f1-score']]
                    newData = np.round(newData, 4)

                    self.pdf.add_page()
                    self.pdf.set_font("Arial", 'B', 20)
                    self.pdf.rect(5.0, 5.0, 200.0, 287.0)
                    self.pdf.rect(8.0, 8.0, 194.0, 282.0)
                    self.pdf.cell(60)
                    self.pdf.set_xy(65.0, 15.0)
                    self.pdf.cell(75, 10, "Sentimental Analysis", 0, 2, 'C')
                    self.pdf.cell(90, 10, '', 0, 2, 'C')
                    self.pdf.cell(-55)
                    self.pdf.cell(60)
                    self.pdf.set_xy(65.0, 30.0)
                    self.pdf.cell(75, 10, str(model), 0, 2, 'C')
                    self.pdf.set_xy(70.0, 45.0)
                    self.pdf.set_font("Arial", 'B', 12)
                    self.pdf.cell(45, 10, "Accuracy Score is: ", 1, 0, 'C')
                    self.pdf.cell(20, 10, str(round(accuracyScore, 4)), 1, 1, 'C')
                    self.pdf.set_xy(70.0, 55.0)
                    self.pdf.cell(45, 10, "Precision Score is: ", 1, 0, 'C')
                    self.pdf.cell(20, 10, str(round(precisionScore, 4)), 1, 1, 'C')
                    self.pdf.set_xy(70.0, 65.0)
                    self.pdf.cell(45, 10, "Recall Score is: ", 1, 0, 'C')
                    self.pdf.cell(20, 10, str(round(recallScore, 4)), 1, 1, 'C')
                    self.pdf.set_xy(70.0, 75.0)
                    self.pdf.cell(45, 10, "F1Score is: ", 1, 0, 'C')
                    self.pdf.cell(20, 10, str(round(f1Score, 4)), 1, 1, 'C')
                    self.pdf.cell(60)
                    self.pdf.set_xy(15.0, 90.0)
                    self.pdf.cell(60)
                    self.pdf.set_font("Arial", 'B', 15)
                    self.pdf.cell(60, 15, txt="Classification Report", ln=1, align='C')

                    self.pdf.set_xy(35.0, 105.0)
                    self.pdf.set_font("Arial", 'B', 12)
                    colNameList = list(newData.columns)
                    for name in colNameList:
                        self.pdf.cell(35, 10, name, 1, 0, 'C')

                    self.pdf.cell(-105)
                    self.pdf.set_xy(35.0, 115.0)

                    for row in range(0, len(newData)):
                        for colNum, colName in enumerate(colNameList):
                            if colNum != len(colNameList) - 1:
                                self.pdf.cell(35, 10, str(newData['%s' % colName].iloc[round(row, 4)]), 1, 0, 'C')
                            else:
                                self.pdf.cell(35, 10, str(newData['%s' % colName].iloc[round(row, 4)]), 1, 2, 'C')
                                self.pdf.cell(-105)

                    self.pdf.cell(60)
                    self.pdf.set_xy(70.0, 150.0)
                    self.pdf.set_font("Arial", 'B', 15)
                    self.pdf.cell(60, 15, txt="Confusion Matrix", ln=1, align='C')

                    for image in os.listdir("Documents/"):
                        if image.split("_")[0] == data[0]:
                            self.pdf.set_xy(30.0, 160.0)
                            self.pdf.image("Documents/" + image, x=None, y=None, w=600 / 5, h=300 / 5, link='', type='')

            self.pdf.output("Documents/EvaluationReport.pdf")

        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception Occured in generatePDF: %s' % e)
            self.logger_object.log(self.file_object, 'generatePDF method .Exited !!')
            raise e