from PredictionRawDataValidation.predictionRawValidation import PredictionRawDataValidation
from DataTransformPrediction.dataTransformationPrediction import dataTransformPredict
from ApplicationLogging.logger import AppLogger


class PredictionValidation:

    def __init__(self, path, file):
        self.rawData = PredictionRawDataValidation(path, file)
        self.file = file
        self.dataTransform = dataTransformPredict()
        self.file_object = open("PredictionLogs/PredictionMainLog.txt", "a+")
        self.log_writer = AppLogger()

    def predictionValidation(self):
        try:
            self.log_writer.log(self.file_object, "Start Validation on files!!!")

            LengthOfDataTimestamp, ColNames, NumberOfColumns = self.rawData.valuesFromSchema()
            regex = self.rawData.manualRegex()

            self.rawData.validateFileNameRaw(regex, LengthOfDataTimestamp)
            self.rawData.validateColumnLength(NumberOfColumns)

            self.log_writer.log(self.file_object, "Raw Data Validation Complete!!")
            self.log_writer.log(self.file_object, "Starting Data Transforamtion!!")

            self.dataTransform.replaceMissingValueWithNull(None)

            self.log_writer.log(self.file_object, "DataTransformation Completed!!!")
            self.log_writer.log(self.file_object,
                                "Creating PredictionDatabase and tables on the basis of given schema!!!")

            self.log_writer.log(self.file_object, "Moving bad files to Archive and deleting BadData folder!!!")

            self.rawData.moveBadFilesToArchiveBad()
            self.log_writer.log(self.file_object, "Bad files moved to archive!! Bad folder Deleted!!")
            self.log_writer.log(self.file_object, "Validation Operation completed!!")

            self.file_object.close()

        except Exception as e:
            raise e