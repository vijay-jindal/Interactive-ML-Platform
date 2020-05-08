import pandas as pd

class Dataset:
    """docstring for Dataset."""
    def __init__(self, app, path):
        self.app = app
        self.path = path
        # Empty cells are not converted to NaN
        self.df = pd.read_csv(self.path, na_filter=False)
        self.app.logger.info("Instance for Dataset Created")

    def info(self):
        return (self.df.columns,self.df.dtypes)

    def set_features(self, list):
        self.X = self.df[list].copy()
        self.app.logger.info(self.X)

    def set_target(self, list):
        self.y = self.df[list].copy()
        self.app.logger.info(self.y)

    def get_features(self):
        return self.X

    def get_target(self):
        return self.y

    def missing_value_indicator(self, placeholders):
        # Create a new column in df1 to indicate if a row has missing values as per defined placeholders
        # References : https://stackoverflow.com/q/50845987
        print(placeholders)
        print(self.df['fixed acidity'])
        x = self.df.astype(str).apply((lambda row, placeholders=placeholders: "true" if any(
            placeholder == field for field in row for placeholder in placeholders) else "false"), axis=1)
        print(x)
        return x
