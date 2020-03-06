from flask import (
    Flask, render_template, request,
    jsonify)
from services import pre_process, algorithm_select, hyperparameter_select

app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('dashboard.html')


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


@app.route('/hyperparameter', methods=['POST', 'GET'])
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
