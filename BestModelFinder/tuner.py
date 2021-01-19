from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from sklearn.metrics  import roc_auc_score,accuracy_score
from sklearn.metrics import confusion_matrix, precision_score, recall_score
from sklearn import model_selection
from sklearn.ensemble import BaggingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.multiclass import OneVsRestClassifier

class ModelFinder:

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.rfCl = RandomForestClassifier()
        self.xgb = XGBClassifier()
        self.mnb = MultinomialNB()
        self.ovrModel = OneVsRestClassifier(self.xgb)

    def getBestParamsForRandomForest(self, trainX, trainY):
        
        self.logger_object.log(self.file_object, 'entered in the getBestParamsForRandomForest of the ModelFinder class')
        try:
            self.paramaGrid = {
                'n_estimators': [10,50,100,130], 'criterion': ['gini','entropy'],
                'max_depth': range(2,5,1), 'max_features': ['auto', 'log2']
            }
            self.grid = GridSearchCV(estimator = self.rfCl, param_grid = self.paramGrid, cv = 5, verbose = 3)
            self.grid.fit(trainX, trainY)

            self.criterion = self.grid.best_params_['criterion']
            self.n_estimators = self.grid.best_params_['n_estimators']
            self.max_depth = self.grid.best_params_['max_depth']
            self.max_features = self.grid.best_params_['max_features']

            self.rfCl = RandomForestClassifier(n_estimators = self.n_estimators, criterion = self.criterion,
                max_depth = self.max_depth, max_features = self.max_features)
            
            self.rfCl.fit(trainX, trainY)
            self.logger_object.log(self.file_object,
                'Best Paramas for RandomForest: ' + str(self.grid.best_params_) +'. Exited the getBestParamsForRandomForest of the ModelFinder class'
            )

            return self.rfCl

        except Exception as e:
            self.logger_object.log(self.file_object,
                'Exception occured in getBestParamsForRandomForest method of the Model_Finder class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                'Random Forest Parameter tuning  failed. Exited the getBestParamsForRandomForest method of the Model_Finder class')
            raise Exception()

    def getBestParamsForXgBoost(self, trainX, trainY):

        self.logger_object.log(self.file_object, 'Entered in the getBestParamsForXgBoost of the ModelFinder class')
        try:
            self.paramGridXgBoost = {
                'learning_rate': [0.5, 0.1, 0.01, 0.001],
                'max_depth': [3, 5, 10, 20],
                'n_estimators': [10, 50, 100, 200]
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

            self.logger_object.log(self.file_object,
                'Best params for XgBoost: ' + str(self.grid.best_params_) + '. Exited from the getBestParamsForXgBoost of the ModelFinder class')
            
            return self.xgb
            
        except Exception as e:
            self.logger_object.log(self.file_object,
                'Exception occured in getBestParamsForXgBoost method of the Model_Finder class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                'XGBoost Parameter tuning  failed. Exited the getBestParamsForXgBoost method of the Model_Finder class')
            raise Exception()

    def getBestBaggingClassifier(self, trainX, trainY):
        self.logger_object.log(self.file_object,
            'Entered in the getBestParamsForBaggingClassifier of the ModelFinder class')
        try:
            self.seed = 8
            self.kfold = model_selection.KFold(n_splits = 3, random_state = self.seed)

            self.model = BaggingClassifier(base_estimator = self.mnb, n_estimators = 10)
            self.model.fit(trainX, trainY)

            self.logger_object.log(self.file_object,
                'Exited from getBestBaggingClassifier of the ModelFinder class')

            return self.model
        except Exception as e:
            self.logger_object.log(self.file_object,
                'Exception occured in getBestBaggingClassifier method of the Model_Finder class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                'BaggingClassifier creation failed. Exited the getBestBaggingClassifier method of the Model_Finder class')
            raise Exception()

    def getBestModel(self. trainX, trainY, testX, testY):

        self.logger_object.log(self.file_object,
            'Entered the getBestMode of the ModelFindef class')

        try:
            self.xgBoost = self.getBestParamsForXgBoost(trainX, trainY)
            self.predictionXgBoost = self.xgBoost.predict(testX, testY)

            self.randomForest = self.getBestParamsForRandomForest(trainX, trainY)
            self.predictionRandomForest = self.randomForest(testX, testY)

            self.baggingClassifier = self.getBestBaggingClassifier(trainX, trainY)
            self.predictionBClassifier = self.baggingClassifier(testX, testY)

            if len(testY.unique()) == 1:
                self.xgBoostScore = accuracy_score(testY, self.predictionXgBoost)
                self.logger_object.log(self.file_object, 
                    'Accuracy Score of xgBoost: ' + str(self.xgBoostScore))

                self.randomForestScore = accuracy_score(testY, self.predictionRandomForest)
                self.logger_object.log(self.file_object,
                    'Accuracy Score of RandomForest: ' + str(self.randomForestScore))

                self.BClassifierScore = accuracy_score(testY, self.predictionBClassifier)
                self.logger_object.log(self.file_object,
                    'Accuracy Score of BClassifier: ' + str(self.BClassifierScore))
            else:
                self.xgBoostScore = roc_auc_score(testY, self.predictionXgBoost)
                self.logger_object.log(self.file_object,
                    'RocAuc Score of xgBoost: ' + str(self.predictionXgBoost))

                self.randomForestScore = roc_auc_score(testY, self.predictionRandomForest)
                self.logger_object.log(self.file_object,
                    'RocAuc Score of RandomForest: ' + str(self.randomForestScore))

                self.BClassifierScore = roc_auc_score(testY, self.predictionBClassifier)
                self.logger_object.log(self.file_object,
                    'RocAuc Score of BClassifier: ' + str(self.BClassifierScore))

            if self.randomForestScore > self.xgBoostScore and self.randomForestScore > self.BClassifierScore:
                return 'RandomForest', self.randomForest
            elif self.xgBoostScore > self.randomForestScore and self.xgBoostScore > self.BClassifierScore:
                return 'XgBoost', self.xgBoost
            else:
                return 'BaggingClassifier', self.baggingClassifier

        except Exception as e:
            self.logger_object.log(self.file_object,
                'Exception occured in get_best_model method of the Model_Finder class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                'Model Selection Failed. Exited the get_best_model method of the Model_Finder class')
            raise Exception()
