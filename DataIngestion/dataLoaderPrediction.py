import pandas as pd
import os

class DataGetterPred:

    def __init__(self, file_object, logger_object):
        self.prediction_dir = 'PredictionBatchFiles/'
        self.file_object = file_object
        self.logger_object = logger_object

    def getData(self, file):

        self.logger_object.log(self.file_object, 
            'Entered in the getData of the DataGetterPred class')

        try:
            data = pd.read_csv(self.prediction_dir + file)
            self.logger_object.log(self.file_object,
                'Data Load Succesfully. Exited to getData of the DataGetterPred class')

            return data
        except Exception as e:
            self.logger_object.log(self.file_object,
                'Exception occured in getData method of the DataGetterPred class. Exception message: '+str(e))
            self.logger_object.log(self.file_object,
                'Data Load Unsuccessful.Exited the getData method of the DataGetterPred class')
            raise Exception()
