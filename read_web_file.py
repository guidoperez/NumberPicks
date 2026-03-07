import sys
import re
import os

"""
read all content from file ff_web_file.txt or .html and write CSV rows.

Usage: execute after get_web_data.py. The default behavior reads
html_files/fantasy_five.html and writes to
data_files/fantasy_five_data_file.csv. Paths can be overridden by
passing input and output paths to `ff_to_csv` or via command-line
arguments.
"""


def ff_to_csv(input_path=None, output_path=None):
    """Extracts dates and numbers from an HTML file and writes CSV.

    Args:
        input_path (str|None): Path to input HTML file. If None, defaults
            to html_files/fantasy_five.html relative to this script.
        output_path (str|None): Path to output CSV file. If None, defaults
            to data_files/fantasy_five_data_file.csv relative to this script.
    """
    base_dir = os.path.dirname(__file__)
    if input_path is None:
        input_path = os.path.join(base_dir, 'html_files', 'fantasy_five.html')
    if output_path is None:
        output_path = os.path.join(base_dir, 'data_files', 'fantasy_five_data_file.csv')

    date_re = re.compile(r'(\d{1,2}/\d{1,2}/\d{2,4})')
    num_re = re.compile(r'>(\d{1,2})<')

    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
    except OSError as e:
        print(f"Error creating output directory: {e}")
        return

    try:
        with open(input_path, 'rt', encoding='utf-8', errors='ignore') as infile, \
                open(output_path, 'w', encoding='utf-8', newline='') as outfile:

            row = []
            for line in infile:
                dmatch = date_re.search(line)
                if dmatch:
                    # start a new row with the date
                    row = [dmatch.group(1)]
                    continue

                nmatch = num_re.search(line)
                if nmatch and row:
                    row.append(nmatch.group(1))
                    # when we have date + 6 numbers (7 fields) write the row
                    if len(row) >= 7:
                        outfile.write(','.join(row[:7]) + '\n')
                        row = []

    except FileNotFoundError:
        print(f"Input file not found: {input_path}")
    except OSError as e:
        print(f"File error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == '__main__':
    input_path = sys.argv[1] if len(sys.argv) > 1 else None
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    ff_to_csv(input_path, output_path)