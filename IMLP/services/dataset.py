import pandas as pd
import numpy as np
import uuid
from sklearn.impute import SimpleImputer


class Dataset:
    """docstring for Dataset."""

    def __init__(self, app, path):
        self.app = app
        self.path = path
        # Empty cells are not converted to NaN
        self.df = pd.read_csv(self.path, na_filter=False)
        self.header = pd.read_csv(self.path, header=None, nrows=1).iloc[0]
        self.app.logger.info("Instance for Dataset Created")
        self.identifier = uuid.uuid4().hex

    def info(self):
        return (self.df.columns, self.df.dtypes)

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
        x = self.df.astype(str).apply((lambda row, placeholders=placeholders: "true" if any(
            placeholder == field for field in row for placeholder in placeholders) else "false"), axis=1)
        return x

    # def duplicate_column_name_check(self, df):
    #     if self.header.duplicated().to_list().count(True) > 0:
    #         all_columns = df.columns.to_list()
    #         duplicated_column_boolean_list = self.header.duplicated().to_list()
    #         list_of_duplicated_columns = [j for i,j in enumerate(all_columns) if(duplicated_column_boolean_list[i] == True)]
    #         return True, list_of_duplicated_columns
    #     else:
    #         return False,[]

    def duplicate_column_check(self, df):
        if self.header.duplicated(keep='last').to_list().count(True) == 0:
            return False, []
        else:
            dfT = df.T
            dfT['duplicate-columns'] = self.header.to_list()
            duplicate_column_position = [pos for pos in range(0, len(self.header.to_list())) if dfT.duplicated()[pos]]
            print(duplicate_column_position)
            print(self.header.to_list())
            if len(duplicate_column_position) == 0:
                return False, []
            else:
                return True, duplicate_column_position

    def duplicate_rows_check(self, df):
        return df.duplicated().astype(str)

    def missing_value_imputer(self, df, value, strategy):
        # TODO: Check for categorical data
        df.replace(value, np.nan, inplace=True)
        df[:] = SimpleImputer(missing_values=np.nan, strategy=strategy).fit_transform(df.values)
        return df
