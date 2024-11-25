import csv
import sys
from csv import reader

from itertools import islice

number_file = open('data_files/jpot_data_file.csv')
#r = csv.reader(number_file)
#total_recs = len(list(r))
total_recs = sum(1 for row in number_file)

f = 1

#while f < total_recs:
#    print("Creating array_" +str(f))
#    f += 1
#print(total_recs)
def get_array_name():
    with open('data_files/jpot_data_file.csv', mode = 'rt') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in islice(csv_reader,10):
            if line_count == 0:
                print(f'Headers {",".join(row)}')
                line_count += 1
            #print(f'\t{row["draw_date"]}_{row["day_of_week"]}')
            arr_name = f'\t{row["draw_date"]}{row["day_of_week"]}'.replace("/","")
            num1,\
            num2,\
            num3,\
            num4,\
            num5,\
            num6,\
            day_of_week = row["num1"],row["num2"],row["num3"],row["num4"],row["num5"],row["num6"],row["day_of_week"]
            #arr_name = [row["num1"],row["num2"],row["num3"],row["num4"],row["num5"]]
            #print(arr_name)
            create_n_fill_array(arr_name, num1, num2, num3, num4, num5, num6, day_of_week)

            line_count += 1
        print(f'Processed {line_count} lines.')

def create_n_fill_array(arr_name,num1,num2,num3,num4,num5,num6,dow):
    arr_name = []
    arr_name.append(num1)
    arr_name.append(num2)
    arr_name.append(num3)
    arr_name.append(num4)
    arr_name.append(num5)
    arr_name.append(num6)
    arr_name.append(dow)

    print(arr_name)


get_array_name()
#create_n_fill_array()


#with open(number_file,'rt') as read_obj:
#    for each_row in read_obj:
