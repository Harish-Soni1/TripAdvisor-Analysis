import pickle
import os
import shutil

class FileOperations:

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.modelDirectory = 'Models/'

    def saveModel(self, model, filename):

        self.logger_object.log(self.file_object,
            "Entered int the saveModel if the FileOperations class")

        try:
            if filename == 'svm':
                fullFilename = 'SupportVector'
            elif filename == 'rf':
                fullFilename = 'RandomForest'
            elif filename == 'xg':
                fullFilename = 'XGBoost'
            elif filename == 'bnb':
                fullFilename = 'BaggingGaussianNB'
            else:
                fullFilename = filename

            path = os.path.join(self.modelDirectory, fullFilename)
            if os.path.isdir(path):
                shutil.rmtree(self.modelDirectory)
                os.mkdir(path)
            else:
                os.mkdir(path)

            with open(path + "/" + fullFilename + ".sav", 'wb') as file:
                pickle.dump(model, file)
            
            self.logger_object.log(self.file_object,
                'Model File '+filename+' saved. Exited the save_model method of the Model_Finder class')
            
            return 'success'

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in save_model method of the Model_Finder class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                'Model File '+filename+' could not be saved. Exited the save_model method of the Model_Finder class')
            raise Exception()

    def loadModel(self, filename):

        self.logger.log(self.file_object, 
            'Entered in the loadModel of the FileOperation class')

        try:
            with open(self.modelDirectory + filename + "/" + filename + ".sav", 'rb') as file:
            
                self.logger_object.log(self.file_object,
                    'Model File ' + filename + ' loaded. Exited the load_model method of the Model_Finder class')
            
            return pickle.load(file)

        except Exception as e:
            self.logger_object.log(self.file_object,
                'Exception occured in load_model method of the Model_Finder class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                'Model File ' + filename + ' could not be saved. Exited the load_model method of the Model_Finder class')
            raise Exception()

    