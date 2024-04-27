# -*- coding: utf-8 -*-
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

from settings import get_settings


def main():
    cfg = get_settings()

    client = Client(cfg.binance_api_key, cfg.binance_secret_key)

    tickers_raw = client.get_all_tickers()
    # ticker = client.get_ticker(symbol="BTCUSDT")
    tickers = {}
    for item in tickers_raw:
        tickers[item["symbol"]] = item["price"]

    print(tickers.keys())


if __name__ == "__main__":
    main()
