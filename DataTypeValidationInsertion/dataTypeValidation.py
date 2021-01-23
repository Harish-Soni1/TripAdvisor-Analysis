import shutil
import pymongo
from datetime import datetime
from os import listdir
import os
import csv
import json
from ApplicationLogging.logger import AppLogger

class dBOperation:
 
    def __init__(self):
        self.path = 'TrainingDatabase/'
        self.badFilePath = "TrainingRawFilesValidated/BadRaw"
        self.goodFilePath = "TrainingRawFilesValidated/GoodRaw"
        self.client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
        self.logger = AppLogger()

    def dataBaseConnection(self, DatabaseName):

        try:
            conn = self.client[DatabaseName] 
            file = open("TrainingLogs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Opened %s database successfully" % DatabaseName)
            file.close()

        except ConnectionError:
            file = open("TrainingLogs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Error while connecting to database: %s" %ConnectionError)
            file.close()
            raise ConnectionError

        return conn

    def createTableDb(self,DatabaseName,column_names):

        try:
            conn = self.dataBaseConnection(DatabaseName)
            collectionList = conn.collection_names()

            if "Training" in collectionList:
                
                self.client.close()
                
                file = open("TrainingLogs/DataBaseCollectionCreateLog.txt", 'a+')
                self.logger.log(file, "Collection created successfully!!")
                file.close()

                file = open("TrainingLogs/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Closed %s database successfully" % DatabaseName)
                file.close()

            else:
                conn.create_collection("GoodRawData",
                {
                    Comments: <string>,
                    Ratings: <string>
                })
            
                self.client.close()

                file = open("TrainingLogs/DataBaseTableCreateLog.txt", 'a+')
                self.logger.log(file, "Table created successfully!!")
                file.close()

                file = open("TrainingLogs/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Closed %s database successfully" % DatabaseName)
                file.close()

        except Exception as e:
            file = open("TrainingLogs/DataBaseTableCreateLog.txt", 'a+')
            self.logger.log(file, "Error while creating table: %s " % e)
            file.close()
            
            self.client.close()

            file = open("TrainingLogs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Closed %s database successfully" % DatabaseName)
            file.close()
            raise e


    def insertIntoTableGoodData(self,Database):

        conn = self.dataBaseConnection(Database)
        goodFilePath= self.goodFilePath
        badFilePath = self.badFilePath
        onlyfiles = [f for f in listdir(goodFilePath)]
        log_file = open("TrainingLogs/DataBaseInsertLog.txt", 'a+')

        for file in onlyfiles:
            try:
                conn.Training.drop()

                with open(goodFilePath+'/'+file, "r") as csvFile:
                    next(csvFile)
                    reader = csv.DictReader(csvFile)
                    for line in reader:
                        row = {}
                        for field in ['Comments', 'Ratings']:
                            try:
                                row[field] = line[field]
                            except Exception as e:
                                raise e
                        conn.Training.insert(row)

            except Exception as e:

                self.logger.log(log_file,"Error while creating table: %s " % e)
                shutil.move(goodFilePath+'/' + file, badFilePath)
                
                self.logger.log(log_file, "File Moved Successfully %s" % file)
                log_file.close()
                
                self.client.close()

        self.client.close()
        log_file.close()

    def selectingDatafromtableintocsv(self,Database):

        self.fileFromDb = 'TrainingFileFromDB/'
        self.fileName = 'InputFile.csv'
        log_file = open("TrainingLogs/ExportToCsv.txt", 'a+')

        try:
            conn = self.dataBaseConnection(Database)
            sqlSelect = "SELECT * FROM GoodRawData"
            cursor = conn.cursor()

            cursor.execute(sqlSelect)

            results = cursor.fetchall()
            headers = [i[0] for i in cursor.description]

            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            csvFile = csv.writer(open(self.fileFromDb + self.fileName, 'w', newline=''),delimiter=',', lineterminator='\r\n',quoting=csv.QUOTE_ALL, escapechar='\\')

            csvFile.writerow(headers)
            csvFile.writerows(results)

            self.logger.log(log_file, "File exported successfully!!!")
            log_file.close()

        except Exception as e:
            self.logger.log(log_file, "File exporting failed. Error : %s" %e)
            log_file.close()

