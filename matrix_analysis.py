# read line by line of csv file and fill a matrix
# get all the numbers for friday
import csv
import pandas as pd


# open the csv file to read it
def read_csv_output_file():
    load_mtx = []

    df = (pd.read_csv('/Users/guidoperez/Repositories/NumberPicks/data_files/Final_jpot_data_file.csv')
            [lambda x: x['day_of_week'] == 'Friday'])

    get_mtx_data = df.iloc[0:2,1:7]


    load_mtx = load_mtx.append(get_mtx_data)

    print(load_mtx)



read_csv_output_file()

