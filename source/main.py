import os
from dotenv import load_dotenv
from binance.cm_futures import CMFutures

load_dotenv()


bn_secret = os.getenv("BN_SECRET")
bn_key = os.getenv("BN_KEY")
bn_api_url = os.getenv("BN_API_URL")


clt = CMFutures(key=bn_secret, secret=bn_secret, base_url=bn_api_url)
