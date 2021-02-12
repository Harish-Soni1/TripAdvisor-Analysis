from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from sklearn import model_selection
from sklearn.ensemble import BaggingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier

class ModelFinder:

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.rfCl = RandomForestClassifier()
        self.xgb = XGBClassifier()
        self.mnb = MultinomialNB()
        self.svc = SVC()
        self.ovrModel = OneVsRestClassifier(self.xgb)

    def getBestParamsForRandomForest(self, trainX, trainY):
        
        self.logger_object.log(self.file_object, 'entered in the getBestParamsForRandomForest of the ModelFinder class')
        try:
            self.paramaGrid = {
                'n_estimators': [10, 50, 100, 130], 'criterion': ['gini', 'entropy'],
                'max_depth': range(2, 5, 1), 'max_features': ['auto', 'log2']
            }
            self.grid = GridSearchCV(estimator = self.rfCl, param_grid = self.paramaGrid, cv = 5, verbose = 3)
            self.grid.fit(trainX, trainY)

            self.criterion = self.grid.best_params_['criterion']
            self.n_estimators = self.grid.best_params_['n_estimators']
            self.max_depth = self.grid.best_params_['max_depth']
            self.max_features = self.grid.best_params_['max_features']

            self.rfCl = RandomForestClassifier(n_estimators = self.n_estimators, criterion = self.criterion,
                max_depth = self.max_depth, max_features = self.max_features)
            
            self.rfCl.fit(trainX, trainY)

            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,
                'Best Paramas for RandomForest: ' + str(self.grid.best_params_) +'. Exited the getBestParamsForRandomForest of the ModelFinder class'
            )
            file.close()

            return self.rfCl

        except Exception as e:
            self.logger_object.log(self.file_object,
                'Exception occured in getBestParamsForRandomForest method of the ModelFinder class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                'Random Forest Parameter tuning  failed. Exited the getBestParamsForRandomForest method of the ModelFinder class')
            raise e

    def getBestParamsForXgBoost(self, trainX, trainY):

        self.logger_object.log(self.file_object, 'Entered in the getBestParamsForXgBoost of the ModelFinder class')
        try:
            self.paramGridXgBoost = {
                'learning_rate': [0.01, 0.001],
                'max_depth': [10, 20],
                'n_estimators': [100, 200]
            }

            self.grid = GridSearchCV(estimator = XGBClassifier(objective = 'multi:softmax'), param_grid = self.paramGridXgBoost,
                cv = 5, verbose = 3)
            self.grid.fit(trainX, trainY)

            self.learning_rate = self.grid.best_params_['learning_rate']
            self.n_estimators = self.grid.best_params_['n_estimators']
            self.max_depth = self.grid.best_params_['max_depth']

            self.xgb = XGBClassifier(n_estimators = self.n_estimators, learning_rate = self.learning_rate,
                max_depth = self.max_depth, objective = 'multi:softmax')
            self.xgb.fit(trainX, trainY)

            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,
                'Best params for XgBoost: ' + str(self.grid.best_params_) + '. Exited from the getBestParamsForXgBoost of the ModelFinder class')
            file.close()
            return self.xgb
            
        except Exception as e:
            self.logger_object.log(self.file_object,
                'Exception occured in getBestParamsForXgBoost method of the ModelFinder class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                'XGBoost Parameter tuning  failed. Exited the getBestParamsForXgBoost method of the ModelFinder class')
            raise e

    def getBestBaggingClassifier(self, trainX, trainY):
        self.logger_object.log(self.file_object,
            'Entered in the getBestParamsForBaggingClassifier of the ModelFinder class')
        try:
            self.seed = 8
            self.kfold = model_selection.KFold(n_splits = 3, random_state = self.seed)

            self.model = BaggingClassifier(base_estimator = self.mnb, n_estimators = 10)
            self.model.fit(trainX, trainY)

            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,
                'Exited from getBestBaggingClassifier of the ModelFinder class')
            file.close()

            return self.model
        except Exception as e:
            self.logger_object.log(self.file_object,
                'Exception occured in getBestBaggingClassifier method of the ModelFinder class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                'BaggingClassifier creation failed. Exited the getBestBaggingClassifier method of the ModelFinder class')
            raise e

    def bestOnvsRestClassifierModel(self, trainX, trainY):

        self.logger_object.log(self.file_object,
            'Entered in the bestOnevsRestClassifier of the ModelFinder class')

        try:
            self.xgBoost = self.getBestParamsForXgBoost(trainX, trainY)
            self.ovrModel = OneVsRestClassifier(self.xgBoost)
            self.ovrModel.fit(trainX, trainY)

            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,
                'Exited from bestOnevsRestClassifier of the ModelFinder class')
            file.close()

            return self.ovrModel
        except Exception as e:
            self.logger_object.log(self.file_object,
                'Exception occured in bestOnevsRestClassifier method of the ModelFinder class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                'OnevsRstClassifier creation failed. Exited the bestOnevsRestClassifier method of the ModelFinder class')
            raise e

    def bestParaMeterForSupportVector(self, trainX, trainY):

        self.logger_object.log(self.file_object,
                               'Entered in the bestParaMeterForSupportVector of the ModelFinder class')

        try:
            self.paramaGridSVC = {
                'C': [0.1, 1, 10, 100, 1000],
                'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
                'kernel': ['rbf']
            }
            self.grid = GridSearchCV(estimator = self.svc, param_grid = self.paramaGridSVC,
                cv = 5, verbose = 3)
            self.grid.fit(trainX, trainY)

            self.C = self.grid.best_params_['C']
            self.gamma = self.grid.best_params_['gamma']
            self.kernel = ['rbf']

            self.svc = SVC( C = self.C, gamma = self.gamma, kernel = self.kernel)
            self.svc.fit(trainX, trainY)

            file = open('TrainingLogs/GeneralLog.txt', 'a+')
            self.logger_object.log(file,
                'Best params for SupportVector: ' + str(self.grid.best_params_) + '. Exited from the bestParaMeterForSupportVector of the ModelFinder class')
            file.close()

            return self.svc

        except Exception as e:
            self.logger_object.log(self.file_object,
                'Exception occured in bestParaMeterForSupportVector method of the ModelFinder class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                'SupprtVectorMachine Parameter tuning failed. Exited the bestParaMeterForSupportVector method of the ModelFinder class')
            raise e

