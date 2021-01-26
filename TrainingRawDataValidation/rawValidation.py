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
        self.logger = App_Logger()

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
            message ="LengthOfDateTimeStampInFile:: %s" %LengthOfDateTimeStampInFile +"\t " + "NumberofColumns:: %s" % NumberofColumn + "\n"
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
                os.mkdir(path)
            path = os.path.join("TrainingRawFilesValidated/","BadRaw/")
            if not os.path.exists(path):
                os.mkdir(path)

        except OSError as ex:
            file = open("TrainingLogs/GeneralLog.txt", 'a+')
            self.logger.log(file,"Error while creating Directory %s:" % ex)
            file.close()
            raise OSError
    def deleteExistingGoodDataTrainingFolder(self):
        try:
            path = "TrainingRawFilesValidated/"
            if os.path.exists(path + "GoodRaw/"):
                shutil.rmtree(path + "GoodRaw/")
                file = open("Training_Logs/GeneralLog.txt", 'a+')
                self.logger.log(file,"GoodRaw directory deleted successfully!!!")
                file.close()

        except OSError as s:
            file = open("TrainingLogs/GeneralLog.txt", 'a+')
            self.logger.log(file,"Error while Deleting Directory : %s" %s)
            file.close()
            raise OSError

    def deleteExistingBadDataTrainingFolder(self):
        try:
            path = "TrainingRawFilesValidated/"
            if os.path.exists(path + "BadRaw/"):
                shutil.rmtree(path + "BadRaw/")
                file = open("Training_Logs/GeneralLog.txt", 'a+')
                self.logger.log(file,"BadRaw directory deleted successfully!!!")
                file.close()

        except OSError as s:
            file = open("Training_Logs/GeneralLog.txt", 'a+')
            self.logger.log(file,"Error while Deleting Directory : %s" %s)
            file.close()
            raise OSError

    def moveBadFilesToArchivedBad(self):

        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")

        try:
            source = "TrainingRawFilesValidated/BadRaw/"

            if os.path.isdir(source):
                path = "TrainingArchivedBadData"
                if not os.path.exists(path):
                    os.mkdir(path)
                
                destPath = "TrainingArchivedBadData/BadData_" + str(date) + "_" + str(time)
                if not os.path.exists(destPath):
                    os.mkdir(destPath)
                
                files = os.listdir(source)
                for file in files:
                    if file not in os.listdir(destPath):
                        shutil.move(source + file, destPath)

                file = open("TrainingLogs/GeneralLog.txt", 'a+')
                self.logger.log(file,"Bad files moved to archive")
                path = 'TrainingRawFilesValidated/'
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

        onlyfiles = [f for f in listdir(self.Batch_Directory)]
        try:
            file = open("TrainingLogs/nameValidationLog.txt", "a+")
            for filename in onlyfiles:
                if re.match(regex, filename):
                    splitAtDot = re.split(".csv", filename)
                    if len(splitAtDot[1]) == LengthOfDateTimeStampInFile:
                        shutil.copy("TrainingBatchFiles/" + filename, "TrainingRawFilesValidated/GoodRaw")
                        self.logger.log(f,"Valid File name!! File moved to GoodRaw Folder :: %s" % filename)
                    else:
                        shutil.copy("TraininBatchFiles/" + filename, "TariningRawFilesValidated/BadRaw")
                        self.logger.log(f,"Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                else:
                    shutil.copy("TraininBatchFiles/" + filename, "TariningRawFilesValidated/BadRaw")
                    self.logger.log(f,"Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
            
            f.close()

        except Exception as e:
            f = open("Training_Logs/nameValidationLog.txt", 'a+')
            self.logger.log(f, "Error occured while validating FileName %s" % e)
            f.close()
            raise e

    def validateColumnLength(self, NumberOfColumn):
        try:
            file = open("TariningLogs/columnValidationLog.txt", "a+")
            self.logger.log(f,"Column Length Validation Started!!")
            for filename in listdir("TrainingRawFilesValidated/GoodRaw"):
                csv = pd.read_csv("TrainingRawFilesValidated/GoodRaw/" + filename)
                if csv.shape[1] == NumberOfColumn:
                    pass
                else:
                    shutil.move("TrainingRawFilesValidated/GoodRaw/" + filename, "TariningRawFilesValidated/BadRaw")
                    self.logger.log(f, "Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)
            self.logger.log(f, "Column Length Validation Completed!!")

        except OSError:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Error Occured while moving the file :: %s" % OSError)
            f.close()
            raise OSError

        except Exception as e:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Error Occured:: %s" % e)
            f.close()
            raise e

        f.close()

    