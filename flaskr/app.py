from flask import (
    Flask, render_template, request,
    jsonify)
from services import pre_process, algorithm_select, hyperparameter_select

app = Flask(__name__)

'''
    Input :
            GET : None
    Output:
            GET : Dashboard.html
'''
@app.route('/')
def welcome():
    return render_template('dashboard.html')


'''
    Input :
            GET  : None
            POST : dataset_path as String, project_name as String, target_feature as String
    Output:
            GET  : upload-csv.html + project name + target variable
            POST : Processed Dataset path, null exceptions, dataset exceptions, etc.
'''
@app.route('/project', methods=['POST', 'GET'])
def project():
    if request.method == 'GET':
        return render_template('upload-csv.html')

    if request.method == 'POST':
        try:
            dataset_path = request.form['dataset_path']
            project_name = request.form['project_name']
            target_feature = request.form['target_feature']
            return pre_process.main(dataset_path, project_name, target_feature)
        except:
            return "Invalid Parameters"

'''
    Input :
            GET  : None
            POST : Algorithm Name as String
    Output:
            GET  : Select algorithm page
            POST : List of Hyperparameters for that algorithm with default values
'''
@app.route('/algorithm', methods=['POST', 'GET'])
def algorithm():
    if request.method == 'GET':
        return "Select the Algorithm"

    if request.method == 'POST':
        try:
            algorithm_name = request.form['algorithm_name']
            return algorithm_select.getHyperparameters(algorithm_name)
        except:
            return "Invalid Parameters"

'''
    Input :
            POST : algorithm_name as a String and hyperparameters as a JSON object
    Output:
            POST : Page to ask for training and testing dataset split ratio and
            other additional inputs and then run the algorithms.
'''
@app.route('/hyperparameter', methods=['POST'])
def hyperparameterUpdate():
    if request.method == 'GET':
        return "Enter values for Hyperparameters"

    if request.method == 'POST':
        try:
            algorithm_name = request.form['algorithm_name']
            hyperparameters_data = request.form['hyperparameters']
            return hyperparameter_select.updateHyperparameters(algorithm_name, hyperparameters_data)
        except:
            return "Invalid Parameters"


if __name__ == '__main__':
    app.run(debug=True)
