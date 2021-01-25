from datetime import datetime
from TrainingRawDataValidation.rawValidation import RawDataValidation
from DataTypeValidationInsertion.dataTypeValidation import dBOperation
from DataTransform.dataTransformation import dataTransform
from ApplicationLogging.logger import AppLogger

class TrainValidation:

    def __init__(self, path):
        self.rawData = RawDataValidation(path)
        self.dataTransform = dataTransform()
        self.dBOperation = dBOperation()
        self.file_object = open("TrainingLogs/TrainingMainLog.txt", "a+")
        self.log_writer = AppLogger()

    def trainValidation(self):
        try:
            self.log_writer.log(self.file_object, "Start Validation on files!!!")

            LengthOfDataTimestamp, ColNames, NumberOfColumns = self.rawData.valuesFromSchema()
            regex = self.rawData.manualRegEx()

            self.rawData.validateFileNameRaw(regex, LengthOfDataTimestamp)
            self.rawData.validateColumnLength(NumberOfColumns)
            
            self.log_writer.log(self.file_object, "Raw Data Validation Complete!!")
            self.log_writer.log(self.file_object, "Starting Data Transforamtion!!")

            self.dataTransform.replaceMissingValueWithNull(None)

            self.log_writer.log(self.file_object, "DataTransformation Completed!!!")
            self.log_writer.log(self.file_object,
                "Creating Training_Database and tables on the basis of given schema!!!")

            self.dBOperation.createTableDb("Training")
            self.log_writer.log(self.file_object, "Table creation Completed!!")
            self.log_writer.log(self.file_object, "Insertion of Data into Table started!!!!")

            self.dBOperation.insertIntoTableGoodData("Training")
            self.log_writer.log(self.file_object, "Insertion in Table completed!!!")
            self.log_writer.log(self.file_object, "Deleting Good Data Folder!!!")

            self.rawData.deleteExistingGoodDataTrainingFolder()
            self.log_writer.log(self.file_object, "Good_Data folder deleted!!!")
            self.log_writer.log(self.file_object, "Moving bad files to Archive and deleting Bad_Data folder!!!")

            self.rawData.moveBadFilesToArchivedBad()
            self.log_writer.log(self.file_object, "Bad files moved to archive!! Bad folder Deleted!!")
            self.log_writer.log(self.file_object, "Validation Operation completed!!")
            self.log_writer.log(self.file_object, "Extracting csv file from table")

            self.dBOperation.selectingDatafromtableintocsv("Training")
            self.file_object.close()

        except Exception as e:
            raise e