"""Extract draw date and numbers from file PDF and write CSV.

Usage:
    python read_pdf_file.py [pdf_path] [output_csv]

.
If no `output_csv` is provided, defaults to
`data_files/cash_4_life_data_file.csv`.

Requires: PyPDF2 (install with `pip install PyPDF2`).
"""
import os
import sys
import re
import csv

try:
    from PyPDF2 import PdfReader
except Exception:
    print("PyPDF2 is required. Install with: pip install PyPDF2")
    sys.exit(1)


def extract_draws_from_text(text):
    """Return list of tuples: (date_string, [num1..num5], cb)

    Strategy: find date occurrences (MM/DD/YY or MM/DD/YYYY format), then 
    for each date, skip ahead and find the next six numeric tokens, treating 
    first five as main numbers and sixth as CB. This handles table-layout PDFs 
    where dates appear in columns.
    
    Key fix: Avoid matching concatenated dates by ensuring the date is on its
    own (preceded by a newline or start of text).
    """
    # Match MM/DD/YY or MM/DD/YYYY, but ensure it's not part of a larger number
    # sequence (e.g., won't match "2511" from "11/29/2511/29/25")
    # This pattern requires that the date be preceded by start-of-line or non-digit
    date_re = re.compile(r"(?:^|[^\d])(\d{1,2}/\d{1,2}/\d{2,4})(?:[^\d]|$)")
    # Match 1-2 digit numbers at word boundaries
    num_re = re.compile(r"\b(\d{1,2})\b")

    draws = []
    seen_dates = set()

    for dmatch in date_re.finditer(text):
        date_str = dmatch.group(1)
        if date_str in seen_dates:
            continue
        
        # find numbers after the date
        # Skip to the next line to avoid grabbing components of the current date
        rest_of_text = text[dmatch.end():]
        newline_pos = rest_of_text.find('\n')
        
        if newline_pos != -1:
            search_start = dmatch.end() + newline_pos + 1
        else:
            search_start = dmatch.end() + 1
        
        nums = []
        for nmatch in num_re.finditer(text, search_start):
            num_str = nmatch.group(1)
            # Florida Lotto numbers are 1-53; skip numbers outside this range
            # (like day/year parts if we're still in a date)
            try:
                num_val = int(num_str)
                # Allow 0-59 range to be safe (includes possible future rule changes)
                if 0 <= num_val <= 59:
                    nums.append(num_str)
            except ValueError:
                pass
            
            if len(nums) >= 6:
                break

        if len(nums) >= 6:
            main = nums[:5]
            cb = nums[5]
            draws.append((date_str, main, cb))
            seen_dates.add(date_str)

    return draws


def read_pdf(path):
    """Extract text from all pages of a PDF and return as a single string."""
    try:
        reader = PdfReader(path)
    except FileNotFoundError:
        raise
    except Exception as e:
        raise RuntimeError(f"Failed to open PDF '{path}': {e}")

    texts = []
    for page in reader.pages:
        try:
            texts.append(page.extract_text() or "")
        except Exception:
            # page extraction may fail; keep going
            texts.append("")

    return "\n".join(texts)


def write_csv(draws, out_path):
    """Write draws to CSV with header draw_date,num1..num5,CB"""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['draw_date', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6'])
        for date_str, main, cb in draws:
            writer.writerow([date_str] + main + [cb])


def main(pdf_path=None, out_csv=None):
    base_dir = os.path.dirname(__file__)
    if pdf_path is None:
        pdf_path = os.path.join(base_dir, 'pdf_files', 'l6.pdf')
    if out_csv is None:
        out_csv = os.path.join(base_dir, 'data_files', 'fla_lotto_data_file.csv')

    if not os.path.exists(pdf_path):
        print(f"PDF not found: {pdf_path}")
        sys.exit(1)

    try:
        text = read_pdf(pdf_path)
    except Exception as e:
        print(e)
        sys.exit(1)

    draws = extract_draws_from_text(text)
    if not draws:
        print("No draws found in PDF text. The extraction heuristics may need adjustment.")
        sys.exit(1)

    write_csv(draws, out_csv)
    print(f"Wrote {len(draws)} draws to {out_csv}")


if __name__ == '__main__':
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else None
    out_csv = sys.argv[2] if len(sys.argv) > 2 else None
    main(pdf_path, out_csv)
