import pandas as pd
import numpy as np
import os
import json
import environmentVariable
from flask import jsonify
import shutil


def null_check(data):
    null_columns = data.columns[data.isnull().any()]
    print(data[null_columns].isnull())
    return "Success"


def feature_check():
    return "Success"


def read_data(path):
    data = pd.read_csv(path)
    return data


def nans(df):
    df = df.fillna(axis=1, value=0)
    dfx = df[df.isnull().any(axis=1)]
    print(len(dfx))
    return df


def main(path, name,target_feature):
    dirx = "/Users/vijayjindal/PycharmProjects/IMLP/" + name
    if not os.path.exists(dirx):
        os.mkdir(dirx)
    data = pd.DataFrame()
    newPath = shutil.copy(path, dirx)

    try:
        data = read_data(newPath)
    except None:
        return "Dataset Not found"

    try:
        print(null_check(data))
        return "Success"
    except None:
        return "Null values"
