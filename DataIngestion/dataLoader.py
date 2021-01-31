import pandas as pd

class DataGetter:

    def __init__(self, file_object, logger_object):
        self.predictionFile = "TrainingfileFromDB/InputFile.csv"
        self.file_object = file_object
        self.logger_object = logger_object

    def getData(self):

        self.logger_object.log(self.file_object, 
            'Entered in the getData of the DataGetter class')

        try:
            self.data = pd.read_csv(self.predictionFile)

            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,
                'Data Load Succesfully. Exited to getData of the DataGetter class')
            file.close()

            return self.data

        except Exception as e:
            self.logger_object.log(self.file_object,
                'Exception occured in getData method of the DataGetter class. Exception message: '+str(e))
            self.logger_object.log(self.file_object,
                'Data Load Unsuccessful.Exited the getData method of the DataGetter class')
            raise e
