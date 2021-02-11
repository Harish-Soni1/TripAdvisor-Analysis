from wsgiref import simple_server
from flask import Flask,render_template,request,Response,send_file
import os
import pandas as pd
import shutil
from flask_cors import cross_origin,CORS
from trainingModel import TrainingModel
from trainValidationInsertion import TrainValidation
import flask_monitoringdashboard as dashboard
from predictionValidationInsertion import PredictionValidation
from predictionFromModel import PredictionFromModel
from zipfile import ZipFile

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

application = Flask(__name__)
dashboard.bind(application)
CORS(application)

@application.route("/",methods=['GET'])
@cross_origin()
def home():
    already_exist = None
    if os.path.exists('Models/'):
        file = os.listdir('Models/')
        if 'SupportVectorMachine' in file:
            exist = 'svm'
        elif 'RandomForest' in file:
            exist = 'rf'
        elif 'XGBoost' in file:
            exist = 'xg'
        elif 'BaggingMultinomialNB' in file:
            exist = 'bnb'
        else:
            exist = 'none'
        already_exist = {'model': exist}
    return render_template('index.html', already_exist=already_exist)

@application.route("/trainModel",methods=['POST'])
@cross_origin()
def trainModelRoute():
    try:
        if request.method == 'POST':
            try:
                if request.form is not None:
                    if request.form['model_list[]'] is not None and request.form['sampler'] is not None:
                        model_list = request.form.getlist('model_list[]')
                        sampling = request.form['sampler']

                        for file in os.listdir("TrainingLogs"):
                            filePath = os.path.join("TrainingLogs/", file)
                            try:
                                if os.path.isfile(filePath) or os.path.islink(filePath):
                                    os.unlink(filePath)
                                elif os.path.isdir(filePath):
                                    shutil.rmtree(filePath)
                            except Exception as e:
                                raise  e

                        trainObj = TrainValidation("TrainingBatchFiles/")
                        trainObj.trainValidation()
                        trainModelObj = TrainingModel(model_list, sampling)
                        trainModelObj.trainModel()
                return Response('Training Completed Successfully !!!!')
            except ValueError:
                print(str(ValueError))
                return Response('Error Occured! %s' % str(ValueError))
            except KeyError:
                print(str(KeyError))
                return Response('Error Occured! %s' % str(KeyError))
        else:
            print('None Request Method Passed')
        return Response("Model Creation Succesfull")
    except Exception as e:
        print(e)
        raise e


@application.route("/predictBatch",methods=['POST'])
@cross_origin()
def predictBatchRoute():
    try:
        if request.method == 'POST':
            try:
                response = 0

                for file in os.listdir("PredictionLogs"):
                    filePath = os.path.join("PredictionLogs/", file)
                    try:
                        if os.path.isfile(filePath) or os.path.islink(filePath):
                            os.unlink(filePath)
                        elif os.path.isdir(filePath):
                            shutil.rmtree(filePath)
                    except Exception as e:
                        raise e

                if 'batchfile[]' in request.files:

                    for file in os.listdir("PredictionBatchFiles"):
                        filePath = os.path.join("PredictionBatchFiles/", file)
                        try:
                            if os.path.isfile(filePath) or os.path.islink(filePath):
                                os.unlink(filePath)
                            elif os.path.isdir(filePath):
                                shutil.rmtree(filePath)
                        except Exception as e:
                            raise e

                    batchFiles = request.files.getlist("batchfile[]")
                    for file in batchFiles:
                        file.save('PredictionBatchFiles/' + file.filename)
                        predictionValidation = PredictionValidation('PredictionBatchFiles', file.filename)
                        predictionValidation.predictionValidation()
                    for file in os.listdir("PredictionBatchFiles/"):
                        prediction = PredictionFromModel()
                        response = prediction.predictData(file)

                    if response == 1:
                        return Response('Bulk Batch Prediction Completed Successfully !!!')
                    else:
                        return Response('Error while doing Bulk Batch Prediction !!!')

            except Exception as e:
                print(e)
                raise e
            return Response('File Uploaded Successfully!!')
    except Exception as e:
        print(e)
        return Response('Error Occured::%s'%str(e))


@application.route("/predictRow",methods=['POST'])
@cross_origin()
def predictRowRoute():
    try:
        if request.method == 'POST':
            try:
                if request.form is not None:
                    if request.form['comment'] is not None:

                        for file in os.listdir("PredictionLogs"):
                            filePath = os.path.join("PredictionLogs/", file)
                            try:
                                if os.path.isfile(filePath) or os.path.islink(filePath):
                                    os.unlink(filePath)
                                elif os.path.isdir(filePath):
                                    shutil.rmtree(filePath)
                            except Exception as e:
                                raise e

                        comment = list()
                        comment.append(request.form['comment'])
                        prediction = PredictionFromModel()
                        data = pd.DataFrame({'Comment': comment})
                        response = prediction.PredictRowData(data)
                        return Response(response)
            except Exception as e:
                raise e
    except Exception as e:
        print(e)
        return Response('Error Occured::%s' % str(e))


@application.route("/download_prediction",methods=['GET'])
@cross_origin()
def download_prediction():
    try:
        file_paths = list()
        list_files = [i for i in os.listdir('PredictedFiles')]
        for f in list_files:
            file_paths.append('PredictedFiles/' + f)

        if file_paths is not None:
            with ZipFile('PredictionZip/Prediction.zip','w') as zip:
                for file in file_paths:
                    zip.write(file)

            if os.path.exists('PredictedFiles'):
                file = os.listdir('PredictedFiles')
                if not len(file) == 0:
                    for f in file:
                        os.remove('PredictedFiles/' + f)
            else:
                pass

        file = os.listdir('PredictionZip')[0]
        return send_file('PredictionZip/' + file, as_attachment=True)

    except Exception as e:
        print(e)
        raise e


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    httpd = simple_server.make_server(host,port,application)
    httpd.serve_forever()

