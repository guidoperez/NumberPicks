import csv
import random

import numpy as np


def sample():
    with open('/Users/guidoperez/Repositories/NumberPicks/data_files/Final_jpot_data_file.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile)
        next(spamreader)
        list_of = []
        j = 0
        lines = [line for line in spamreader]
        for i in range(len(lines)):
            list_ = []
            if len(lines) <= i + j:
                break
            first = lines[i + j][0]
            while first == lines[i + j][0]:
                list_.append(lines[i + j][2])
                j += 1
                if len(lines) <= i + j:
                    break
            j -= 1
            list_of.append(list(map(float, list_)))

    maxlen = len(max(list_of))
    print("\t" + "\t".join([str(el) for el in range(1, maxlen + 1)]) + "\n")
    for i in range(len(list_of)):
        print(str(i + 1) + "\t" + "\t".join([str(el) for el in list_of[i]]) + "\n")


def read_data():
    with open('/Users/guidoperez/Repositories/NumberPicks/data_files/Final_jpot_data_file.csv', 'r') as csvfile:

        spamreader = csv.reader(csvfile)

        next(spamreader)

        lines = [line for line in spamreader]

#        print(lines[0:2]) >>> [['08/25/23', '3', '8', '17', '20', '30', '32', 'Friday'], ['01/31/23', '2', '5', '6', '12', '35', '42', 'Tuesday']]

#        print(lines[0][1:7]) >>> ['3', '8', '17', '20', '30', '32']

        mtrx = []

        for r in range(len(lines)):
            mtrx.append(lines[r][1:7])

#        print("printing " + str(len(lines)) + " rows")
#        print(np.matrix(mtrx))
#        result_set = '\n'.join([''.join(['{:5}'.format(item) for item in row]) for row in mtrx])
#        print(result_set)

        results = dict(zip(*np.unique(mtrx, return_counts=True)))

        by_val = dict(sorted(results.items(), key=lambda item:item[1], reverse=True))

#        print(by_val)

        [print(key, ':', value) for key, value in by_val.items()]

#        print(results)


def play_numbers():
    cmb_1 = [2, 3, 10, 17, 27, 46]

    cmb_2 = [9, 12, 13, 19, 31, 41]

    cmb_3 = [15, 16, 18, 34, 40, 45]

    cmb_4 = [1, 24, 26, 36, 42, 43]

    cmb_5 = [6, 7, 8, 11, 22, 44]

    all_cmb = [cmb_1, cmb_2, cmb_3, cmb_4, cmb_5]

    cmb_num_1 = random.choice(cmb_1)

    print(cmb_num_1)

    #print(random.randint(cmb_2))


#read_data()
#play_numbers()
#sample()