import pandas

import os

def mock_garden_log(path=''):
    if not path:
        path = os.path.join(os.path.split(os.path.realpath('__name__'))[0], 'test_files/garden_log.csv')
    df = pandas.read_csv(path)
    return df

