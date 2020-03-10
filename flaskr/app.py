"""
Please note for logging use the app's logger functionality
Refer to this : https://flask.palletsprojects.com/en/1.1.x/logging/ and
https://docs.python.org/3/library/logging.html#logging-levels
Ex: app.logger.info("Message")
"""

from flask import (
    Flask, render_template, request, redirect
)
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

@app.route('/project/<project_name>')
def new_project(project_name):
    project.create(project_name)
    return redirect('/project/'+project_name+'/upload')

@app.route('/project/<project_name>/upload',methods=['GET','POST'])
def upload(project_name):
    if request.method == 'GET':
        if hasattr(project,"name") and project_name == getattr(project,"name"):
            return render_template('upload-csv.html')
        else:
            return redirect('/')
    elif request.method == 'POST' and 'dataset' in request.files:
        project.upload_dataset(request.files['dataset']) # allow only csv files in UI
        # TODO : create instance of dataset class
        return redirect('/project/'+project_name+'/preprocess')
    else:
        return redirect('/')

@app.route('/project/<project_name>/preprocess')
def preprocess(project_name):
    if request.method == 'GET':
        if hasattr(project,"name") and project_name == getattr(project,"name"):
            return "WIP"
            # return render_template('preprocess.html')
        else:
            return redirect('/')
    return "WIP"

if __name__ == '__main__':
    app.run(debug=True)
