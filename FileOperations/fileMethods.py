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
                os.makedirs(path)
            else:
                os.makedirs(path)

            with open(path + "/" + fullFilename + ".pkl", 'wb') as file:
                pickle.dump(model, file)
                file.close()

            logfile = open("TrainingLogs/GeneralLogs.txt", 'a+')
            self.logger_object.log(logfile,
                'Model File '+filename+' saved. Exited the save_model method of the Model_Finder class')
            logfile.close()
            
            return 'success'

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in save_model method of the Model_Finder class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                'Model File '+filename+' could not be saved. Exited the save_model method of the Model_Finder class')
            raise Exception()

    def loadModel(self, filename=None):

        self.logger_object.log(self.file_object,
            'Entered in the loadModel of the FileOperation class')

        try:
            if filename:
                with open(self.modelDirectory + filename + "/" + filename + ".pkl", 'rb') as file:

                    self.logger_object.log(self.file_object,
                        'Model File ' + filename + ' loaded. Exited the load_model method of the Model_Finder class')

                    return pickle.load(file)
            else:
                model_dir = os.listdir(self.modelDirectory)
                model_name = os.listdir(self.modelDirectory + model_dir[0])
                model_name = model_name[0].split('.')[0]
                with open(self.modelDirectory + model_name + "/" + model_name + ".pkl", 'rb') as file:
                    self.logger_object.log(self.file_object,
                                           'Exited the find_correct_model_file method of FileMethods Package')
                    return pickle.load(file)

        except Exception as e:
            self.logger_object.log(self.file_object,
                'Exception occured in load_model method of the Model_Finder class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                'Model File ' + filename + ' could not be saved. Exited the load_model method of the Model_Finder class')
            raise Exception()

    