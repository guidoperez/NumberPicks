import urllib.request
import ssl
import imaplib

#Adding SSL upgrade authentication handshake issue in python3.10
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.set_ciphers('DEFAULT')
ctx.verify_mode = ssl.CERT_NONE


def get_web_data():
    # Retrieve the .html
    fantasy_five = 'https://www.flalottery.com/exptkt/ff.htm'
    fl_lotto = 'https://flalottery.com/exptkt/l6.htm'
    cash_4_life = 'https://flalottery.com/exptkt/c4l.htm'
    jackpot = 'https://www.flalottery.com/exptkt/jtp.htm'

    # get all games in a list
    games = [jackpot]

    # web_url = fantasy_five_url

    for game_file in games:

        open_webpage = urllib.request.urlopen(game_file, context = ctx)

        read_web_pagedata = open_webpage.read()  # reads the_ .htm file

        # Multiple lines to write files if found in list

        # Write an .html file ff_web_file.html with the data read from the FL website
        open('html_files/jpot_web_file.html', 'wb+').write(read_web_pagedata)


if __name__ == '__main__':
    get_web_data()
