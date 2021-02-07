from fpdf import FPDF
import os

class PDF:

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object


    def generatePDF(self, dict):
        file = open('TrainingLogs/GeneralLog.txt', 'a+')
        self.logger_object.log(file,
            'Entered generatePDF method of PDF class')
        file.close()

        try:
            self.pdf = FPDF()
            self.pdf.add_page()
            self.pdf.set_font("Arial", size=15)
            self.pdf.set_fill_color(32.0, 47.0, 250.0)
            self.pdf.rect(5.0, 5.0, 200.0, 287.0, 'DF')
            self.pdf.set_fill_color(255, 255, 255)
            self.pdf.rect(8.0, 8.0, 194.0, 282.0, 'FD')
            i=0

            for data in dict:
                if data[1]['AccuracyScore'] is not None:
                    if data[0] == 'svm':
                        model = "Support Vector Machine"
                    elif data[0] == 'bnb':
                        model = "Bagging Classifier"
                    elif data[0] == 'xgb':
                        model = "XGBoost"
                    else:
                        model = "Random Forest"
                    accuracyScore = data[1]['AccuracyScore']
                    precisionScore = data[1]['PrecisionScore']
                    recallScore = data[1]['RecallScore']
                    f1Score = data[1]['F1Score']
                    clsRepost = data[1]['ClassificationReport']

                    self.pdf.cell(200, 15, txt="Your Model {} is {}".format(i + 1, model), align='C')
                    self.pdf.cell(200, 10, txt="Your Model's Accuracy Scroe is: {}".format(accuracyScore), ln=1, align='L')
                    self.pdf.cell(200, 10, txt="Your Model's Precicion Scroe is: {}".format(precisionScore), ln=2, align='L')
                    self.pdf.cell(200, 10, txt="Your Model's Recall Scroe is: {}".format(recallScore), ln=1, align='L')
                    self.pdf.cell(200, 10, txt="Your Model's F1Scroe is: {}".format(f1Score), ln=1, align='L')
                    self.pdf.cell(200, 10, txt="Your Model's Classification Report", align='C')

                    for data in clsRepost:
                        self.pdf.cell(200, 10, txt=str(clsRepost[data]), ln=1, align='L')

                    self.pdf.cell(200, 10, txt="Classification Report", align='C')

                    for image in os.listdir("Documents/"):
                        if image.split("_")[0] == data[0]:
                            self.pdf.image("Documents/" + image, link='', type='', w=700/5, h=700/5)


            self.pdf.output("Documents/EvaluationReport.pdf")

        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception Occured in generatePDF() ')
            self.logger_object.log(self.file_object, 'generatePDF method .Exited !!')
            raise e