import base64
from datetime import datetime
import os,tempfile
from services.dataset import Dataset
from services.model import Model

class Project:
    """docstring for Project."""
    def __init__(self, app):
        self.app = app
        self.app.logger.info("Instance for Project Created")

    def create(self, project_name):
        self.name = project_name # Decide project naming conventions
        self.date_created = datetime.now()
        self.path = tempfile.mkdtemp() # Create a temporary directory and store the path
        self.app.logger.info("Project Name : " + self.name + "Date Created : " + str(self.date_created) + "Path : "+ self.path)

    def upload_dataset(self, dataset,filename):
        dpath = os.path.join(self.path,filename)
        Project.save_file(dpath,dataset)
        self.app.logger.info("Uploaded Dataset to "+ dpath)
        self.dataset = Dataset(self.app,dpath)

    def create_model(self, name):
        self.model = Model(self.app, self.dataset, Model.Classifiers[name])

    @staticmethod
    def save_file(path, content):
        """Decode and store a file uploaded with Plotly Dash."""
        data = content.encode("utf8").split(b";base64,")[1]
        with open(path, "wb") as fp:
            fp.write(base64.decodebytes(data))
