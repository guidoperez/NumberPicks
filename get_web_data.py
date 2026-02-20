"""
Execute first
"""

import urllib.request
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


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python get_web_data.py <game_key>")
        print("Valid game keys: fantasy_five, fl_lotto, cash_4_life, jackpot")
        sys.exit(1)
    
    lottery_game = sys.argv[1]
    get_web_data(lottery_game)
