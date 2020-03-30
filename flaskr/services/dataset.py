import pandas as pd

class Dataset:
    """docstring for Dataset."""
    def __init__(self, app, path):
        self.app = app
        self.path = path
        self.df = pd.read_csv(self.path)
        self.app.logger.info("Instance for Dataset Created")

    def info(self):
        return (self.df.columns,self.df.dtypes)

    def set_features(self, list):
        self.X = self.df[list].copy()
        self.app.logger.info(self.X)

    def set_target(self, list):
        self.y = self.df[list].copy()
        self.app.logger.info(self.y)
