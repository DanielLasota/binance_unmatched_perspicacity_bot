from binance.client import Client
import time
import os
from dotenv import load_dotenv

from stream_core.orderbook_daemon import OrderbookDaemon
from utils.ascii_arts import ascii_arts
from winamp.winamp import Winamp
from credentials_daemon.login import Login
from stream_core.transaction_daemon import TransactionDaemon
from flask_stream_manager.flask_stream_manager import FlaskManager

# api_key, api_secret = Login.get_secret()
os.system('cls')
load_dotenv(os.path.expandvars(r'%USERPROFILE%/binance_unmatched_perspicacity_bot_dev_mode.env'))

api_key, api_secret = os.environ.get('DEV_MODE_API_KEY'), os.environ.get('DEV_MODE_API_SECRET')

client = Client(api_key, api_secret)

flask_daemon = FlaskManager()
flask_daemon.run()

try:
    account_info = client.get_account()['balances']
    print("Successfully retrieved account information.")
except Exception as e:
    print("An error occurred!")
    print(e)
for info in account_info:
    print(info)
    
# print(colors.MAGENTA ,ascii_arts.ascii_art_1, colors.RESET)
# print(colors.CYAN ,ascii_arts.table_prototype, colors.RESET)

orderbook_daemon = OrderbookDaemon()
orderbook_daemon.run('BTCUSDT')
orderbook_daemon.subscribe(flask_daemon)

transaction_daemon = TransactionDaemon()
transaction_daemon.run('BTCUSDT')
transaction_daemon.subscribe(flask_daemon)

flask_daemon.update('dashboardEstimatedTotalBalance', 1888)
flask_daemon.update('dashboardBTCUSDPriceMain', 2137)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass