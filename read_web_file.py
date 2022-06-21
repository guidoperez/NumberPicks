import sys  # import system libraries
import re  # import regular expression library

"""
    read all content from file ff_web_file.txt or .html

    USE:

    :parameter
"""

write_csv_file = open("/Users/guidoperez/Repositories/NumberPicks/data_files/jpot_data_file.csv", "w")

with open('/Users/guidoperez/Repositories/NumberPicks/html_files/jpot_web_file.html', 'rt') as testFile:
    # r_date = re.compile(r'^*\d{1,2}/\d{1,2}/\d{2}.*')
    xtract_date = re.compile(r'(\d{1,2}/\d{1,2}/\d{1,2})')  # Regex to look for and extract the game date MM/DD/YY
    xtract_nums = re.compile(r'\">+(\d{1,2})+<')  # Regex to look for and extract each of the numbers played

    position = 1  # sets the position of each value ([MM/DD/YY],[##],[##],[##],[##],[##],[##])

    for line in testFile:
        l_search = xtract_date.search(line)
        nums = xtract_nums.search(line)

        if l_search:
            # print(l_search.group(1), end=",")
            write_csv_file.write(l_search.group(1) + ',')
            position = 1  # sets date at position 1

        elif nums:
            # print(nums.group(1), end=",")
            write_csv_file.write(nums.group(1) + ',')
            position += 1

            if position == 7:
                write_csv_file.write('\n')
                # print("")


