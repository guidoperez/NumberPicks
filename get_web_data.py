"""
Execute first
"""

import urllib.request
import urllib.parse
import ssl
import sys
import os

# Adding SSL upgrade authentication handshake issue in python3.10
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.set_ciphers('DEFAULT')
ctx.verify_mode = ssl.CERT_NONE


def get_web_data(game_key):
    """
    Retrieves lottery game data from FL Lottery website and saves as HTML file.
    
    Args:
        game_key (str): The lottery game key (fantasy_five, fl_lotto, cash_4_life, jackpot)
    """
    game_dict = {
        'fantasy_five': 'https://www.flalottery.com/exptkt/ff.htm',
        'fl_lotto': 'https://flalottery.com/exptkt/l6.htm',
        'cash_4_life': 'https://flalottery.com/exptkt/c4l.htm',
        'jackpot': 'https://www.flalottery.com/exptkt/jtp.htm'
    }

    # Validate game key
    if game_key not in game_dict:
        print(f"Error: Invalid game key '{game_key}'")
        print(f"Valid options: {', '.join(game_dict.keys())}")
        return

    # Destination folder and file settings
    dest_folder = 'html_files/'
    dest_file_path = os.path.join(dest_folder, f'{game_key}.html')
    game_url = game_dict[game_key]

    # Ensure destination folder exists
    try:
        os.makedirs(dest_folder, exist_ok=True)
    except OSError as e:
        print(f"Error creating directory '{dest_folder}': {e}")
        return

    # Fetch and save the webpage
    try:
        open_webpage = urllib.request.urlopen(game_url, context=ctx)
        read_web_pagedata = open_webpage.read()

        # Write the HTML file
        with open(dest_file_path, 'wb') as f:
            f.write(read_web_pagedata)
        print(f"Successfully saved {game_key} data to {dest_file_path}")

    except urllib.error.URLError as e:
        print(f"Error fetching URL '{game_url}': {e}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code} fetching '{game_url}': {e.reason}")
    except IOError as e:
        print(f"Error writing to file '{dest_file_path}': {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def download_pdf(pdf_url, dest_folder='pdf_files', filename=None):
    """Download a PDF from `pdf_url` and save it to `dest_folder`.

    Args:
        pdf_url (str): Full URL to the PDF file.
        dest_folder (str): Destination folder to save the PDF.
        filename (str|None): Optional filename to use. If None, derived from URL.
    """
    if filename is None:
        parsed = urllib.parse.urlparse(pdf_url)
        filename = os.path.basename(parsed.path) or 'download.pdf'

    dest_path = os.path.join(dest_folder, filename)

    try:
        os.makedirs(dest_folder, exist_ok=True)
    except OSError as e:
        print(f"Error creating directory '{dest_folder}': {e}")
        return

    try:
        resp = urllib.request.urlopen(pdf_url, context=ctx)
        with open(dest_path, 'wb') as out_f:
            # Stream the response in chunks
            while True:
                chunk = resp.read(8192)
                if not chunk:
                    break
                out_f.write(chunk)
        print(f"Successfully downloaded PDF to {dest_path}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code} downloading '{pdf_url}': {e.reason}")
    except urllib.error.URLError as e:
        print(f"Error downloading URL '{pdf_url}': {e}")
    except IOError as e:
        print(f"Error writing to file '{dest_path}': {e}")
    except Exception as e:
        print(f"Unexpected error downloading PDF: {e}")


def download_game_pdf(game_key, dest_folder='pdf_files'):
    """Convenience wrapper to download the Cash4Life PDF from FL Lottery.

    Args:
        game_key (str): Key for the game (e.g., 'c4l', 'lotto', 'jackpot').
        dest_folder (str): Folder where PDF will be saved (default 'pdf_files').
    """

    game_pdf_data = {
        'c4l': 'https://files.floridalottery.com/exptkt/c4l.pdf',
        'lotto': 'https://files.floridalottery.com/exptkt/l6.pdf',
        'jackpot': 'https://files.floridalottery.com/exptkt/jtp.pdf'
    }

    # Validate game key
    if game_key not in game_pdf_data:
        print(f"Error: Invalid game key '{game_key}'")
        print(f"Valid options: {', '.join(game_pdf_data.keys())}")
        return    

    download_pdf(game_pdf_data[game_key], dest_folder=dest_folder)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python get_web_data.py <game_key>")
        print("Valid game keys: fantasy_five, fl_lotto, cash_4_life, jackpot")
        sys.exit(1)
    
    lottery_game = sys.argv[1]
    #get_web_data(lottery_game)

    try:
        download_game_pdf(lottery_game, dest_folder='pdf_files')
    except Exception as e:
        print(f"Failed to download game PDFs: {e}")
