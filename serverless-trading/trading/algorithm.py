
import os

import pandas as pd
from alpaca.data import (
    StockHistoricalDataClient,
)

from alpaca.data.requests import (
    StockBarsRequest,
    TimeFrame,
)
from alpaca.trading import (
    MarketOrderRequest,
    OrderSide,
    TimeInForce,
    TradingClient,
)
from alpaca.trading.models import Position, TradeAccount
import dotenv

dotenv.load_dotenv()

API_KEY = os.getenv("ALPACA_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET")
BASE_URL = "https://paper-api.alpaca.markets/v2"  # paper trading

stock_history_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)


trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)


from tracemalloc import start


def get_history_data(symbol="AAPL", days=182) -> pd.DataFrame:
    # end date in US Eastern Timezone
    end_date = pd.Timestamp.now(tz="US/Eastern")
    end_date = end_date - pd.Timedelta(days=1)  # yesterday
    start_date = end_date - pd.Timedelta(days=days)

    stock_request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Day,
        start=start_date,
        end=end_date,
    )

    bars = stock_history_client.get_stock_bars(stock_request)

    return bars.df


def calculate_ema(
    data: pd.DataFrame, period: int = 9, column: str = "vwap"
) -> pd.Series:
    # shift the day to yesterday and calculate the EMA
    ema = data[column].ewm(span=period, adjust=False).mean()
    return ema

def calculate_rsi(
    data: pd.DataFrame, period: int = 14, column: str = "vwap"
) -> pd.Series:
    delta = data[column].diff()
    gain = (delta.where(delta > 0, 0)).ewm(span=period).mean()
    loss = (-delta.where(delta < 0, 0)).ewm(span=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
  
def get_signals(symbol="AAPL"):
    data = get_history_data(symbol)
    rsi = calculate_rsi(data).shift(1)
    short_ema = calculate_ema(data, 9).shift(1)
    long_ema = calculate_ema(data, 21).shift(1)

    # a series of same length as data, but add 1 to buy/long, -1 to sell/short, 0 to exit
    signals = pd.Series(0, index=data.index)

    for i in range(1, len(data)):
        if rsi.iloc[i] < 30 and long_ema.iloc[i] > short_ema.iloc[i]:
            signals.iloc[i] = 1
        elif rsi.iloc[i] > 70 and long_ema.iloc[i] < short_ema.iloc[i]:
            signals.iloc[i] = -1

    return signals  # this signals could be used for backtesting, but backtesting is not covered here
  

def trade(symbol="AAPL", quantity=1000):
    '''
    This function will trade the stock based on the signals
    In this example, we used fixed quantity of 1000 shares, however, in real trading, you should calculate the quantity based on your account balance and risk management
    '''
    
    
    signals = get_signals(symbol)
    # get latest signal
    latest_signal = signals.iloc[-1]
    if latest_signal == 1 or True:
        # buy/long
        order_request = MarketOrderRequest(
            symbol=symbol,
            qty=quantity,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY,
        )
        trading_client.submit_order(order_request)
    elif latest_signal == -1:
        # sell/short
        order_request = MarketOrderRequest(
            symbol=symbol,
            qty=quantity,
            side=OrderSide.SELL,
            time_in_force=TimeInForce.DAY,
        )
        trading_client.submit_order(order_request)
    else:
        # keep the position
        pass

    return latest_signal

