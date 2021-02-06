from os import listdir
import pandas
from ApplicationLogging.logger import AppLogger


class dataTransformPredict:

    def __init__(self):
        self.goodDataPath = "PredictionRawFilesValidated/GoodRaw"
        self.logger = AppLogger()

    def replaceMissingValueWithNull(self, data=None):

        log_file = open("PredictionLogs/dataTransformLog.txt", 'a+')
        try:
            if data is None:
                onlyfiles = [f for f in listdir(self.goodDataPath)]
                for file in onlyfiles:
                    csv = pandas.read_csv(self.goodDataPath + "/" + file)
                    csv.fillna('NULL', inplace=True)
                    csv['Comments'] = csv['Comments'].str[6:]
                    csv.to_csv(self.goodDataPath + "/" + file, index=None, header=True)
                    self.logger.log(log_file, " %s: File Transformed successfully!!" % file)
            else:
                data = data.fillna('Null', inplace=True)
                self.logger.log(log_file, " %s: File Transformed successfully!!" % log_file)
                return data
        except Exception as e:
            self.logger.log(log_file, "Data Transformation failed because:: %s" % e)
            log_file.close()
        log_file.close()
