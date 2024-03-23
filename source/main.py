import os
from dotenv import load_dotenv
from binance.cm_futures import CMFutures
from enum import Enum
import pandas as pd


load_dotenv()


bn_secret = os.getenv("BN_SECRET")
bn_key = os.getenv("BN_KEY")
bn_api_url = os.getenv("BN_API_URL")


clt = CMFutures(key=bn_secret, secret=bn_secret, base_url=bn_api_url)


class Interval(Enum):
    m1 = "1m"
    m5 = "5m"
    m15 = "15m"
    m30 = "30m"
    h1 = "1h"


def fetch_data(symbol: str, interval: Interval) -> list:
    try:
        resp = clt.klines(symbol=symbol, interval=interval.value)
        print(f"response length: {len(resp)}")
        return resp
    except Exception as exp:
        print(f"fetch_data err: {exp}")
        return []


rows = fetch_data(symbol="BTCUSD_PERP", interval=Interval.m5)
df = pd.DataFrame.from_records(
    data=rows,
    columns=[
        "open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_asset_volume",
        "number_of_trades",
        "taker_by_volume",
        "taker_by_quote_asset_volume",
        "ignore",
    ],
)
df = df.drop(
    columns=[
        "quote_asset_volume",
        "taker_by_volume",
        "taker_by_quote_asset_volume",
        "ignore",
    ]
)


df["open_time"] = pd.to_datetime(df["open_time"])
df["close_time"] = pd.to_datetime(df["close_time"])
df = df.astype({"close": float})

print(df)


SMA_WINDOW_LENGTH = 20
RSI_WINDOW_LENGTH = 7


df["sma"] = df["close"].rolling(SMA_WINDOW_LENGTH).mean()
df["std"] = df["sma"].rolling(SMA_WINDOW_LENGTH).std()
df["bb_upper"] = df["sma"] + 2 * df["std"]
df["bb_lower"] = df["sma"] - 2 * df["std"]


df["delta"] = df["close"].diff()
df["rs"] = df["avg_gain"] / df["avg_loss"]
df["rsi"] = df["rs"].apply(lambda v: 100 - (100 / (v + 1)))


print(df)
