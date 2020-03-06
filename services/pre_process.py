import pandas
import numpy

def null_check():
    return "Success"


def feature_check():
    return "Success"


def main():
    try:
        null_check()
    except:
        return "Null values"

    try:
        return feature_check()
    except:
        return "Bad feature"
