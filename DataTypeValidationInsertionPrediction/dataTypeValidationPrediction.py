import shutil
import pymongo
from datetime import datetime
import pandas as pd
from os import listdir
import os
import csv
from ApplicationLogging.logger import AppLogger


class dBOperation:

    def __init__(self):
        self.badFilePath = "PredictionRawfilesValidated/BadRaw/"
        self.goodFilePath = "PredictionRawfilesValidated/GoodRaw/"
        self.client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
        self.logger = AppLogger()

    def dataBaseConnection(self, DatabaseName):

        try:
            conn = self.client[DatabaseName]
            file = open("PredictionLogs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Opened %s database successfully" % DatabaseName)
            file.close()

        except ConnectionError:
            file = open("PredictionLogs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Error while connecting to database: %s" % ConnectionError)
            file.close()
            raise ConnectionError

        return conn

    def createTableDb(self, DatabaseName):

        try:
            conn = self.dataBaseConnection(DatabaseName)
            collectionList = conn.collection_names()

            if "GoodRawData" in collectionList:

                allData = conn.GoodRawData.find({}, {"_id": 0, "Comments": 1, "Ratings": 1})
                if allData.count() == 0:
                    self.client.close()

                    file = open("PredictionLogs/DataBaseCollectionCreateLog.txt", 'a+')
                    self.logger.log(file, "Collection Already Exists!!")
                    file.close()

                    file = open("PredictionLogs/DataBaseInsertLog.txt", 'a+')
                    self.logger.log(file, "No Data Found!!")
                    file.close()

                    file = open("PredictionLogs/DataBaseConnectionLog.txt", 'a+')
                    self.logger.log(file, "Closed %s database successfully" % DatabaseName)
                    file.close()

                    return

                conn.GoodRawData.remove()
                self.client.close()

                file = open("PredictionLogs/DataBaseCollectionCreateLog.txt", 'a+')
                self.logger.log(file, "Collection Already Exists!!")
                file.close()

                file = open("PredictionLogs/DataBaseInsertLog.txt", 'a+')
                self.logger.log(file, "Data Deletion Successfully!!")
                file.close()

                file = open("PredictionLogs/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Closed %s database successfully" % DatabaseName)
                file.close()

            else:
                conn.create_collection("GoodRawData")

                self.client.close()

                file = open("PredictionLogs/DataBaseCollectionCreateLog.txt", 'a+')
                self.logger.log(file, "Collection created successfully!!")
                file.close()

                file = open("PredictionLogs/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Closed %s database successfully" % DatabaseName)
                file.close()

        except Exception as e:
            file = open("PredictionLogs/DataBaseCollectionCreateLog.txt", 'a+')
            self.logger.log(file, "Error while creating table: %s " % e)
            file.close()

            self.client.close()

            file = open("PredictionLogs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Closed %s database successfully" % DatabaseName)
            file.close()
            raise e

    def insertIntoTableGoodData(self, Database):

        conn = self.dataBaseConnection(Database)
        logFile = open("PredictionLogs/DataBaseInsertLog.txt", 'a+')

        onlyfiles = [file for file in os.listdir(self.goodFilePath)]
        if onlyfiles:
            for f in onlyfiles:
                try:
                    data = pd.read_csv(os.path.join(self.goodFilePath, f))
                    document = [{'Comments': rating, 'Ratings': label} for rating, label in
                                zip(data['Comments'], data['Ratings'])]
                    conn.GoodRawData.insert_many(document)
                except Exception as e:
                    self.logger.log(logFile, "Insertion in Collection Failed. Error: %s" % e)
                    self.logger.log(logFile, "Insertion in Collection Successfully.")
                    logFile.close()
        else:
            print("No files")
        self.client.close()

        self.logger.log(logFile, "Insertion in Collection Successfully.")
        logFile.close()

    def selectingDatafromtableintocsv(self, Database):

        self.fileFromDb = 'PredictionFileFromDB/'
        self.fileName = 'InputFile.csv'
        log_file = open("PredictionLogs/ExportToCsv.txt", 'a+')
        conn = self.dataBaseConnection(Database)

        try:
            conn = self.dataBaseConnection(Database)
            if conn.GoodRawData.count() == 0:
                self.logger.log(log_file, 'No Record in GoodRawData Collection')
                log_file.close()
                return

            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            data = list()
            for row in conn.GoodRawData.find({}, {"_id": 0, "Comments": 1, "Ratings": 1}):
                data.append({'Comments': row['Comments'], 'Ratings': row['Ratings']})

            dataframe = pd.DataFrame(data, columns=['Comments', 'Ratings'])
            dataframe.to_csv(os.path.join(self.fileFromDb, self.fileName), index=None)

            self.logger.log(log_file, 'CSV File Exported Successfully !!!')
            self.logger.log(log_file,
                            'Successfully Executed selectingDatafromtableintocsv method of dbOperation class of dbOperation package')
            log_file.close()

        except Exception as e:
            self.logger.log(log_file, "File exporting failed. Error : %s" % e)
            log_file.close()
