from os import listdir
import pandas
from ApplicationLogging.logger import AppLogger


class dataTransformPredict:

    def __init__(self):
        self.goodDataPath = "PredictionRawFilesValidated/GoodRaw"
        self.logger = AppLogger()

    def replaceMissingWithNull(self):
        try:
            log_file = open("PredictionLogs/dataTransformLog.txt", 'a+')
            onlyfiles = [f for f in listdir(self.goodDataPath)]
            for file in onlyfiles:
                csv = pandas.read_csv(self.goodDataPath + "/" + file)
                csv.fillna('NULL', inplace=True)
                csv['Comments'] = csv['Comments'].str[6:]
                csv.to_csv(self.goodDataPath + "/" + file, index=None, header=True)
                self.logger.log(log_file, " %s: File Transformed successfully!!" % file)

        except Exception as e:
            self.logger.log(log_file, "Data Transformation failed because:: %s" % e)
            log_file.close()
            raise e

        log_file.close()
