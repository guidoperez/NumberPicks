from csv import reader
from csv import writer
import calendar
import re


def add_column_in_csv(input_file, output_file, transform_row):
    """ Append a column in existing csv using csv.reader / csv.writer classes

    add_column_in_csv('data_files/jpot_data_file.csv', 'data_files/jpot_output_file.csv', lambda row, line_num: row.append(get_day(row[0])))

    """
    # https://thispointer.com/python-add-a-column-to-an-existing-csv-file/
    # Open the input_file in read mode and output_file in write mode
    with open(input_file, 'r') as read_obj, \
            open(output_file, 'w', newline='') as write_obj:
        # Create a csv.reader object from the input file object
        csv_reader = reader(read_obj)
        # create a csv.writer object from the output file object
        csv_writer = writer(write_obj)
        # Read each row of the input csv file as list
        for row in csv_reader:
            # Pass the list / row in the transform function to add column text for this row
            transform_row(row, csv_reader.line_num)
            # Write the updated row / list to the output file
            csv_writer.writerow(row)


def get_day(date):
    month, day, year = (int(i) for i in date.split('/'))
    daynumber = calendar.weekday(year, month, day)
    daysofweek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return daysofweek[daynumber]


def clean_rows():
    """ Replace the double comma, for a cleaner record

    """
    # Open output_file.csv, read line by line and replace the ',,' to ','
    # write a new final file
    # write_final_csv = open('/Users/guidoperez/PycharmProjects/NumberAnalysis/Final_number_file.csv', 'w')

    final_file = '/Users/guidoperez/Repositories/NumberPicks/data_files/Final_jpot_data_file.csv'
    # field_names = ['draw_date', 'num1', 'num2', 'num3', 'num4', 'num5', 'day_of_week']

    write_col_names = open(final_file, 'w')
    write_col_names.write("draw_date,num1,num2,num3,num4,num5,num6,day_of_week\n")
    write_col_names.close()

    write_final_csv = open(final_file, 'a')

    with open('data_files/jpot_output_file.csv', 'rt') as pre_file:
        double_comma = re.compile(',,')
        for rec_line in pre_file:
            get_rec = double_comma.search(rec_line)

            if get_rec:
                write_final_csv.write(str.replace(rec_line, ',,', ','))


add_column_in_csv('data_files/jpot_data_file.csv', 'data_files/jpot_output_file.csv', lambda row, line_num: row.append(get_day(row[0])))
clean_rows()


