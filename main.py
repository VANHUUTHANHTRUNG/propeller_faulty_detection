# Data preprocessing
# - Filter by lab time: 2021-04-12 from 9:14 to 9:55
# - Exclude record with rpm value of 0
# - Label data into normal (label code = 0) and faulty (label code = 1)

import os
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# return data with label
def preprocess(path):
    raw = pd.read_json(path, orient='columns')
    raw = raw.drop(['_id', 'updatedAt', '__v'], axis=1)
    raw['createdAt'] = pd.to_datetime(raw['createdAt'], infer_datetime_format=True)
    raw.rename(columns={'createdAt': 'time'}, inplace=True)

    # Filter by DateTime: 2021 - 04 - 12 (both normal and faulty) & rpm != 0
    year2021 = raw[raw['time'].dt.year == 2021]
    year2021 = year2021[year2021['rpm'] != 0]
    normal = year2021[(year2021['time'] > '2021-04-12T09:14:00') & (year2021['time'] < '2021-04-12T09:31:00')]
    faulty = year2021[(year2021['time'] > '2021-04-12T09:31:00') & (year2021['time'] < '2021-04-12T09:55:00')]
    normal.insert(3, 'label', 0)
    faulty.insert(3, 'label', 1)
    df = pd.concat([normal, faulty])

    # Uncomment the code below to drop 'time' column
    # df = df.drop(['time'], axis=1).reset_index(drop=True)

    df.to_csv('cleaned_propeller.csv', index=False)
    return df


if __name__ == '__main__':
    df = preprocess(dir_path + '/propeller.json')
    df.info()
    print(df.head())

