from datetime import datetime
import os,tempfile
from services.dataset import Dataset
from services.model import Model
from dashApp import dashApp

class Project:
    """docstring for Project."""
    def __init__(self, app, appDash):
        self.app = app
        self.appDash = appDash
        self.app.logger.info("Instance for Project Created")

    def create(self, project_name):
        self.name = project_name # Decide project naming conventions
        self.date_created = datetime.now()
        self.path = tempfile.mkdtemp() # Create a temporary directory and store the path
        self.app.logger.info("Project Name : " + self.name + "Date Created : " + str(self.date_created) + "Path : "+ self.path)

    def upload_dataset(self, dataset):
        dpath = os.path.join(self.path,dataset.filename)
        dataset.save(dpath)
        self.app.logger.info("Uploaded Dataset to "+ dpath)
        self.dataset = Dataset(self.app,dpath)

    def create_model(self, name):
        self.model = Model(self.app, self.dataset, Model.Classifiers[name])

    def render_preprocess_app(self):
        dashAppObject = dashApp(self.app, self.dataset, self.appDash)
