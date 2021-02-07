from datetime import datetime
from os import listdir
import os
import re
import json
import shutil
import pandas as pd
from ApplicationLogging.logger import AppLogger

class RawDataValidation:

    def __init__(self, path):
        self.path = path
        self.schemaPath = 'schema_training.json'
        self.logger = AppLogger()

    def valuesFromSchema(self):
        try:
            with open(self.schemaPath, 'r') as f:
                dic = json.load(f)
                f.close()
            pattern = dic['SampleFileName']
            LengthOfDateTimeStampInFile = dic['LengthOFDateStampInFile']
            ColNames = dic['ColName']
            NumberOfColumn = dic['NumberOfColumn']

            file = open("TrainingLogs/valuesFromSchemaValidationLog.txt", "a+")
            message ="LengthOfDateTimeStampInFile:: %s" %LengthOfDateTimeStampInFile +"\t " + "NumberofColumns:: %s" %NumberOfColumn + "\n"
            self.logger.log(file,message)

            file.close()

        except ValueError:
            file = open("TrainingLogs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file,"ValueError:Value not found inside schema_training.json")
            file.close()
            raise ValueError

        except KeyError:
            file = open("TrainingLogs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, "KeyError:Key value error incorrect key passed")
            file.close()
            raise KeyError

        except Exception as e:
            file = open("TrainingLogs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, str(e))
            file.close()
            raise e

        return LengthOfDateTimeStampInFile, ColNames, NumberOfColumn
    
    def manualRegEx(self):
        return "['Review']+['\_'']+[\d]+\.csv"

    def createDirectoryForGoodBadRawData(self):
        try:
            path = os.path.join("TrainingRawfilesValidated/", "GoodRaw/")
            if not os.path.exists(path):
                os.makedirs(path)
            path = os.path.join("TrainingRawfilesValidated/","BadRaw/")
            if not os.path.exists(path):
                os.makedirs(path)

        except OSError as ex:
            file = open("TrainingLogs/GeneralLog.txt", 'a+')
            self.logger.log(file,"Error while creating Directory %s:" % ex)
            file.close()
            raise ex

    def deleteExistingGoodDataTrainingFolder(self):
        try:
            path = "TrainingRawfilesValidated/"
            if os.path.exists(path + "GoodRaw/"):
                shutil.rmtree(path + "GoodRaw/")
                file = open("TrainingLogs/GeneralLog.txt", 'a+')
                self.logger.log(file,"GoodRaw directory deleted successfully!!!")
                file.close()

        except OSError as s:
            file = open("TrainingLogs/GeneralLog.txt", 'a+')
            self.logger.log(file,"Error while Deleting Directory : %s" %s)
            file.close()
            raise s

    def deleteExistingBadDataTrainingFolder(self):
        try:
            path = "TrainingRawfilesValidated/"
            if os.path.exists(path + "BadRaw/"):
                shutil.rmtree(path + "BadRaw/")
                file = open("TrainingLogs/GeneralLog.txt", 'a+')
                self.logger.log(file,"BadRaw directory deleted successfully!!!")
                file.close()

        except OSError as s:
            file = open("TrainingLogs/GeneralLog.txt", 'a+')
            self.logger.log(file,"Error while Deleting Directory : %s" %s)
            file.close()
            raise OSError

    def moveBadFilesToArchivedBad(self):

        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")

        try:
            source = "TrainingRawfilesValidated/BadRaw/"

            if os.path.isdir(source):
                path = "TrainingArchivedBadData"
                if not os.path.exists(path):
                    os.makedirs(path)
                
                destPath = "TrainingArchivedBadData/BadData_" + str(date) + "_" + str(time)
                if not os.path.exists(destPath):
                    os.makedirs(destPath)
                
                files = os.listdir(source)
                for file in files:
                    if file not in os.listdir(destPath):
                        shutil.move(source + file, destPath)

                file = open("TrainingLogs/GeneralLog.txt", 'a+')
                self.logger.log(file,"Bad files moved to archive")
                path = 'TrainingRawfilesValidated/'
                if os.path.isdir(path + 'Bad_Raw/'):
                    shutil.rmtree(path + 'Bad_Raw/')
                self.logger.log(file,"Bad Raw Data Folder Deleted successfully!!")
                file.close()

        except Exception as e:
            file = open("TrainingLogs/GeneralLog.txt", 'a+')
            self.logger.log(file, "Error while moving bad files to archive:: %s" % e)
            file.close()
            raise e

    def validateFileNameRaw(self, regex, LengthOfDateTimeStampInFile):

        self.deleteExistingBadDataTrainingFolder()
        self.deleteExistingGoodDataTrainingFolder()
        self.createDirectoryForGoodBadRawData()

        onlyfiles = [f for f in listdir(self.path)]
        try:
            file = open("TrainingLogs/nameValidationLog.txt", "a+")
            for filename in onlyfiles:
                if (re.match(regex, filename)):
                    splitAtDot = re.split(".csv", filename)
                    splitAtDot = re.split("_", splitAtDot[0])
                    if len(splitAtDot[1]) == LengthOfDateTimeStampInFile:
                        shutil.copy("TrainingBatchFiles/" + filename, "TrainingRawfilesValidated/GoodRaw")
                        self.logger.log(file,"Valid File name!! File moved to GoodRaw Folder :: %s" % filename)
                    else:
                        shutil.copy("TrainingBatchFiles/" + filename, "TrainingRawfilesValidated/BadRaw")
                        self.logger.log(file,"Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                else:
                    shutil.copy("TrainingBatchFiles/" + filename, "TrainingRawfilesValidated/BadRaw")
                    self.logger.log(file,"Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
            
            file.close()

        except Exception as e:
            f = open("TrainingLogs/nameValidationLog.txt", 'a+')
            self.logger.log(f, "Error occured while validating FileName %s" % e)
            f.close()
            raise e

    def validateColumnLength(self, NumberOfColumn):
        try:
            file = open("TrainingLogs/columnValidationLog.txt", "a+")
            self.logger.log(file,"Column Length Validation Started!!")
            for filename in listdir("TrainingRawfilesValidated/GoodRaw"):
                csv = pd.read_csv("TrainingRawfilesValidated/GoodRaw/" + filename)
                if csv.shape[1] > 2:
                    csv = csv.drop(['Unnamed: 2'], axis=1)
                if csv.shape[1] == NumberOfColumn:
                    pass
                else:
                    print(csv.columns)
                    shutil.move("TrainingRawfilesValidated/GoodRaw/" + filename, "TrainingRawFilesValidated/BadRaw")
                    self.logger.log(file, "Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)
            self.logger.log(file, "Column Length Validation Completed!!")

        except OSError as ex:
            f = open("TrainingLogs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Error Occured while moving the file :: %s" % OSError)
            f.close()
            raise ex

        except Exception as e:
            f = open("TrainingLogs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Error Occured:: %s" % e)
            f.close()
            raise e

        file.close()

    