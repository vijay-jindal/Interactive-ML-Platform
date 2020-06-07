import base64
from datetime import datetime
import os,tempfile
from services.dataset import Dataset
from services.model import Model
import pickle

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

    def create_model(self, type, name):
        if type == "Supervised":
            self.model = Model(self.app, self.dataset, type, Model.Classifiers[name])
        elif type == "Unsupervised":
            self.model = Model(self.app, self.dataset, type, Model.Clusterers[name])
        else:
            self.app.logger.info("Learning type is not valid")

    def save_model(self):
        if self.model.learning_type == "Supervised":
            pickle.dump(self.model.classifier, open(os.path.join(self.path,"model-" + self.date_created.strftime("%Y%m%d%H%M%S") + ".sav"), 'wb'))
        elif self.model.learning_type == "Unsupervised":
            pickle.dump(self.model.clusterer, open(os.path.join(self.path,"model-" + self.date_created.strftime("%Y%m%d%H%M%S") + ".sav"), 'wb'))
        else:
            self.app.logger.info("Learning type is not valid")

    @staticmethod
    def save_file(path, content):
        """Decode and store a file uploaded with Plotly Dash."""
        data = content.encode("utf8").split(b";base64,")[1]
        with open(path, "wb") as fp:
            fp.write(base64.decodebytes(data))
