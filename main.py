import sys

from binance.client import Client
import time
import os
from dotenv import load_dotenv

from calculator.calculator import Calculator
from cli_daemon.cli_daemon import CLIDaemon
from flask_stream_manager.stream_to_logger import FlaskConsoleLogger
from market_stream_core.orderbook_daemon import OrderbookDaemon
from utils.ascii_arts import ascii_arts
from winamp.winamp import Winamp
from credentials_daemon.login import Login
from market_stream_core.transaction_daemon import TransactionDaemon
from flask_stream_manager.flask_stream_manager import FlaskManager

# api_key, api_secret = Login.get_secret()
os.system('cls')
load_dotenv(os.path.expandvars(r'%USERPROFILE%/binance_unmatched_perspicacity_bot_dev_mode.env'))

api_key, api_secret = os.environ.get('DEV_MODE_API_KEY'), os.environ.get('DEV_MODE_API_SECRET')

client = Client(api_key, api_secret)

flask_manager = FlaskManager()
flask_manager.run()

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
orderbook_daemon.register(flask_manager)

transaction_daemon = TransactionDaemon()
transaction_daemon.run('BTCUSDT')
transaction_daemon.register(flask_manager)

flask_manager.update('dashboardEstimatedTotalBalance', 1888)
flask_manager.update('dashboardBTCUSDPriceMain', 2137)

logger = FlaskConsoleLogger()
logger.register(flask_manager)

cli_daemon = CLIDaemon()
flask_manager.register(cli_daemon)

calculator = Calculator()

cli_daemon.register(calculator)
# main_cli =

sys.stdout = logger

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass