"""
Please note for logging use the app's logger functionality
Refer to this : https://flask.palletsprojects.com/en/1.1.x/logging/ and
https://docs.python.org/3/library/logging.html#logging-levels
Ex: app.logger.info("Message")
"""
Project_name = ""
from flask import (
    Flask, render_template, request, redirect, url_for
)
import requests
from services.project import Project

# create the app
app = Flask(__name__)

# create project instance
project = Project(app)

import logging
app.logger.setLevel(logging.INFO)

@app.route('/')
def imlp():
    return render_template('dashboard.html')

@app.route('/project',methods=['POST'])
def new_project():
    Project_name = request.form['project-name']
    Project_name = project.create(Project_name)
    return redirect('/upload/'+Project_name)

@app.route('/upload/<project_name>',methods=['GET'])
def upload(project_name):
    return render_template('upload-csv.html',proj_name=project_name)
    

@app.route('/preprocess',methods=['POST'])
def preprocess():
    if request.form['dataset'] is not null:
            project.upload_dataset(request.form['dataset'])
            column_names,data_types = project.dataset.info()
            app.logger.info(column_names)
            app.logger.info(data_types)
            app.logger.info(project.dataset.path)
            return render_template('preprocess.html',project_name=Project_name,path=project.dataset.path,column_names=column_names,data_types=data_types)
    else:
            return redirect('/')
    return "WIP"

if __name__ == '__main__':
    app.run(debug=True)
