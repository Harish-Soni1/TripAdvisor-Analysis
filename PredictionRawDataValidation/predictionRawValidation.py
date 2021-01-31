from datetime import datetime
from os import listdir
import os
import re
import json
import shutil
import pandas as pd
from ApplicationLogging.logger import AppLogger

class PredictionRawDataValidation:

    def __init__(self, path):
        self.path = path
        self.schema_path = 'schema_prediction.json'
        self.logger = AppLogger()


    def valuesFromSchema(self):
        try:
            with open(self.schema_path, 'r') as file:
                dic = json.load(file)
                file.close()

            patter = dic['SampleName']
            LengthOfDateTimeStampInFile = dic['LengthOFDateStampInFile']
            ColNames = dic['ColName']
            NumberOfColumn = dic['NumberOfColumn']

            file = open("PredictionLogs/valuesFromSchemaValidationLog.txt", "a+")
            message = "LengthOfDateTimeStampInFile:: %s" % LengthOfDateTimeStampInFile + "\t " + "NumberofColumns:: %s" % NumberOfColumn + "\n"
            self.logger.log(file, message)

            file.close()

        except ValueError:
            file = open("PredictionLogs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, "ValueError:Value not found inside schema_Prediction.json")
            file.close()
            raise ValueError

        except KeyError:
            file = open("PredictionLogs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, "KeyError:Key value error incorrect key passed")
            file.close()
            raise KeyError

        except Exception as e:
            file = open("PredictionLogs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, str(e))
            file.close()
            raise e

        return LengthOfDateTimeStampInFile, ColNames, NumberOfColumn

    def manualRegex(self):
        return "['Review']+['\_'']+[\d]+\.csv"

    def createDirectoryForGoodBadRawData(self):
        try:
            path = os.path.join("PredictionRawfilesValidated/", "GoodRaw/")
            if not os.path.exists(path):
                os.makedirs(path)
            path = os.path.join("PredictionRawfilesValidated/", "BadRaw/")
            if not os.path.exists(path):
                os.makedirs(path)

        except OSError as ex:
            file = open("PredictionLogs/GeneralLog.txt", 'a+')
            self.logger.log(file,"Error while creating Directory %s:" % ex)
            file.close()
            raise ex

    def deleteExistingGoodDataPredictionFolder(self):
        try:
            path = 'PredictionRawFilesValidated/'
            if os.path.isdir(path + 'GoodRaw/'):
                shutil.rmtree(path + 'GoodRaw/')
                file = open("PredictionLogs/GeneralLog.txt", 'a+')
                self.logger.log(file, "GoodRaw directory deleted successfully!!!")
                file.close()
        except OSError as s:
            file = open("PredictionLogs/GeneralLog.txt", 'a+')
            self.logger.log(file, "Error while Deleting Directory : %s" % s)
            file.close()
            raise OSError

    def deleteExistingBadDataPredictionFolder(self):
        try:
            path = "PredictionRawFilesValidated/"
            if os.path.isdir(path + 'BadRaw/'):
                shutil.rmtree(path + 'BadRaw/')
            file = open("PredictionLogs/GeneralLog.txt", 'a+')
            self.logger.log(file, "BadRaw directory deleted successfully!!!")
            file.close()

        except OSError as s:
            file = open("PredictionLogs/GeneralLog.txt", 'a+')
            self.logger.log(file, "Error while Deleting Directory : %s" % s)
            file.close()
            raise OSError

    def moveBadFilesToArchiveBad(self):
        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")
        try:
            path= "PredictionArchivedBadData"
            if not os.path.isdir(path):
                os.makedirs(path)
            source = 'PredictionRawFilesValidated/BadRaw/'
            dest = 'PredictionArchivedBadData/BadData_' + str(date)+"_"+str(time)
            if not os.path.isdir(dest):
                os.makedirs(dest)
            files = os.listdir(source)
            for f in files:
                if f not in os.listdir(dest):
                    shutil.move(source + f, dest)
            file = open("PredictionLogs/GeneralLog.txt", 'a+')
            self.logger.log(file,"Bad files moved to archive")
            path = 'PredictionRawFilesValidated/'
            if os.path.isdir(path + 'BadRaw/'):
                shutil.rmtree(path + 'BadRaw/')
            self.logger.log(file,"Bad Raw Data Folder Deleted successfully!!")
            file.close()
        except OSError as e:
            file = open("PredictionLogs/GeneralLog.txt", 'a+')
            self.logger.log(file, "Error while moving bad files to archive:: %s" % e)
            file.close()
            raise OSError

    def validateFileNameRaw(self, regex, LengthOfDateTimeStampInFile):

        self.deleteExistingBadDataPredictionFolder()
        self.deleteExistingGoodDataPredictionFolder()
        self.createDirectoryForGoodBadRawData()

        onlyfiles = [f for f in listdir(self.path)]
        try:
            file = open("PredictionLogs/nameValidationLog.txt", "a+")
            for filename in onlyfiles:
                if (re.match(regex, filename)):
                    splitAtDot = re.split(".csv", filename)
                    splitAtDot = re.split("_", splitAtDot[0])
                    if len(splitAtDot[1]) == LengthOfDateTimeStampInFile:
                        shutil.copy("PredictionBatchFiles/" + filename, "PredictionRawfilesValidated/GoodRaw")
                        self.logger.log(file, "Valid File name!! File moved to GoodRaw Folder :: %s" % filename)
                    else:
                        shutil.copy("PredictionBatchFiles/" + filename, "PredictionRawfilesValidated/BadRaw")
                        self.logger.log(file, "Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                else:
                    shutil.copy("PredictionBatchFiles/" + filename, "PredictionRawfilesValidated/BadRaw")
                    self.logger.log(file, "Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)

            file.close()

        except Exception as e:
            f = open("PredictionLogs/nameValidationLog.txt", 'a+')
            self.logger.log(f, "Error occured while validating FileName %s" % e)
            f.close()
            raise e
        
    def validateColumnLength(self, NumberOfColumn):
        try:
            file = open("PredictionLogs/columnValidationLog.txt", "a+")
            self.logger.log(file,"Column Length Validation Started!!")
            for filename in listdir("PredictionRawfilesValidated/GoodRaw"):
                csv = pd.read_csv("PredictionRawfilesValidated/GoodRaw/" + filename)
                if csv.shape[1] > 2:
                    csv = csv.drop(['Unnamed: 2'], axis=1)
                if csv.shape[1] == NumberOfColumn:
                    pass
                else:
                    print(csv.columns)
                    shutil.move("PredictionRawfilesValidated/GoodRaw/" + filename, "PredictionRawFilesValidated/BadRaw")
                    self.logger.log(file, "Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)
            self.logger.log(file, "Column Length Validation Completed!!")

        except OSError as ex:
            f = open("PredictionLogs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Error Occured while moving the file :: %s" % OSError)
            f.close()
            raise ex

        except Exception as e:
            f = open("PredictionLogs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Error Occured:: %s" % e)
            f.close()
            raise e

        file.close()

