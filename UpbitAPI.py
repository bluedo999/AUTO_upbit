import pyupbit

access_key = "RtNkYNkqltxtJbE9E9OfI2se4xlWDxxKRx5mrQhO"
secret_key = "FkougvxZA0nnVet6DdNNktj9vXSjpVnDixfe6sxz"

class UpbitAPI:
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key
        self.upbit = pyupbit.Upbit(access_key, secret_key)
    def get_rsi(self, coin, interval="minute30", time=14):
        df = pyupbit.get_ohlcv(coin, interval=interval)
        delta = df["close"].diff()
        ups, downs = delta.copy(), delta.copy()
        ups[ups < 0] = 0
        downs[downs > 0] = 0
        AU = ups.rolling(window=time).mean()
        AD = downs.abs().rolling(window=time).mean()
        RS = AU / AD
        RSI = 100.0 - (100.0 / (1.0 + RS))
        return RSI.iloc[-1]
    def get_moving_average(self, coin, time):
        df = pyupbit.get_ohlcv(coin, interval="minute30")
        ma = df['close'].rolling(window=time).mean()
        return ma.iloc[-1]
    def get_bollinger_bands(self, coin, time, multiplier):
        df = pyupbit.get_ohlcv(coin, interval="minute30")
        ma = df['close'].rolling(window=time).mean()
        mstd = df['close'].rolling(window=time).std()
        upper = ma + multiplier * mstd
        lower = ma - multiplier * mstd
        return upper.iloc[-1], lower.iloc[-1]
    def get_macd(self, coin):
        df = pyupbit.get_ohlcv(coin, interval="minute30")
        exp1 = df['close'].ewm(span=12, adjust=False).mean()
        exp2 = df['close'].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        return macd.iloc[-1], signal.iloc[-1]
    def get_breakout_signal(self, coin, time):
        df = pyupbit.get_ohlcv(coin, interval="minute30")
        highest = df["high"].rolling(window=time).max().iloc[-1]
        if pyupbit.get_current_price(coin) > highest:
            return True
    def buy(self, coin, price, amount):
        return self.upbit.buy_limit_order(coin, price, amount)
    def sell(self, coin, price, amount):
        return self.upbit.sell_limit_order(coin, price, amount)
    def get_current_price(self, coin):
        return pyupbit.get_current_price(coin)
    def get_balance(self, ticker):
        return self.upbit.get_balance(ticker)
    def get_balance_info(self):
        balances = self.upbit.get_balances()
        result = {}
        for b in balances:
            [b['currency']] = {'balance': b['balance'], 'locked': b['locked']}
        return result
    def cancel_order(self, uuid):
        return self.upbit.cancel_order(uuid)
    def get_order(self, uuid):
        return self.upbit.get_order(uuid)
    def get_order_list(self, state):
        return self.upbit.get_order(state=state)
    def main(self):
        ##############################
        ## RSI-based trading system ##
        ##############################
        coin = "KRW-BTC"
        trading = 100000
        strategy = "RSI"  # "RSI" or "moving_average" or "bollinger_bands" or "macd" or "breakout_signal"
        trade_interval = "minute30"  # "minute1" or "minute3" or "minute5" or "minute10" or "minute15" or "minute30" or "minute60" or "day"
        interval_time = 14  # Required for RSI, time period for RSI calculation
        ma_time = 5  # Required for moving_average, time period for moving average calculation
        bb_time = 20  # Required for bollinger_bands, time period for bollinger bands calculation
        bb_multiplier = 2  # Required for bollinger_bands, the number of standard deviations to add and subtract from the moving average
        buy_ratio = 0.5  # Percentage of funds to allocate for buying
        sell_ratio = 0.5  # Percentage of coins to sell
        max_sell_loss_ratio = 0.05  # Maximum acceptable loss ratio for a single sell order
        max_trade_size = 0.1  # Maximum percentage of funds to allocate for a single trade (buy or sell)
            # Run main trading logic
        if strategy == "RSI":
            rsi = self.get_rsi(coin, interval=trade_interval, time=interval_time)
            if rsi <= 30:
                price = self.get_current_price(coin)
                balance = self.get_balance("KRW")
                max_buy_amount = balance * max_trade_size
                buy_amount = max_buy_amount * buy_ratio
                self.buy(coin, price, buy_amount)
            elif rsi >= 70:
                coins = self.get_balance(coin.split("-")[-1])
                max_sell_amount = coins * max_trade_size
                sell_amount = max_sell_amount * sell_ratio
                avg_price = self.get_order_list(state="done")[0]["avg_price"]
                loss_ratio = (price - avg_price) / avg_price
                if loss_ratio <= max_sell_loss_ratio:
                    self.sell(coin, price, sell_amount)
            elif strategy == "moving_average":
                ma = self.get_moving_average(coin, time=ma_time)
                price = self.get_current_price(coin)
                if price > ma:
                    balance = self.get_balance("KRW")
                    max_buy_amount = balance * max_trade_size
                    buy_amount = max_buy_amount * buy_ratio
                    self.buy(coin, price, buy_amount)
                else:
                    coins = self.get_balance(coin.split("-")[-1])
                    max_sell_amount = coins * max_trade_size
                    sell_amount = max_sell_amount * sell_ratio
                    avg_price = self.get_order_list(state="done")[0]["avg_price"]
                    loss_ratio = (price - avg_price) / avg_price
                    if loss_ratio <= max_sell_loss_ratio:
                        self.sell(coin, price, sell_amount)
            elif strategy == "bollinger_bands":
                upper, lower = self.get_bollinger_bands(coin, time=bb_time, multiplier=bb_multiplier)
                price = self.get_current_price(coin)
                if price > upper:
                    balance = self.get_balance("KRW")
                    max_buy_amount = balance * max_trade_size
                    buy_amount = max_buy_amount * buy_ratio
                    self.buy(coin, price, buy_amount)
                elif price < lower:
                    coins = self.get_balance(coin.split("-")[-1])
                    max_sell_amount = coins * max_trade_size
                    sell_amount = max_sell_amount * sell_ratio
                    avg_price = self.get_order_list(state="done")[0]["avg_price"]
                    loss_ratio = (price - avg_price) / avg_price
                    if (loss_ratio <= max_sell_loss_ratio):
                        self.sell(coin, price, sell_amount)
                elif strategy == "macd":
                    macd = self.get_macd(coin, time=trade_interval)
                    if macd > 0:
                        price = self.get_current_price(coin)
                        balance = self.get_balance("KRW")
                        max_buy_amount = balance * max_trade_size
                        buy_amount = max_buy_amount * buy_ratio
                        self.buy(coin, price, buy_amount)
                    elif macd < 0:
                        coins = self.get_balance(coin.split("-")[-1])
                        max_sell_amount = coins * max_trade_size
                        sell_amount = max_sell_amount * sell_ratio
                        avg_price = self.get_order_list(state="done")[0]["avg_price"]
                        loss_ratio = (price - avg_price) / avg_price
                    if loss_ratio <= max_sell_loss_ratio:
                        self.sell(coin, price, sell_amount)
                elif strategy == "breakout_signal":
                    high, low = self.get_breakout_levels(coin, time=trade_interval)
                    price = self.get_current_price(coin)
                    if price > high:
                        balance = self.get_balance("KRW")
                        max_buy_amount = balance * max_trade_size
                        buy_amount = max_buy_amount * buy_ratio
                        self.buy(coin, price, buy_amount)
                    elif price < low:
                        coins = self.get_balance(coin.split("-")[-1])
                        max_sell_amount = coins * max_trade_size
                        sell_amount = max_sell_amount * sell_ratio
                        avg_price = self.get_order_list(state="done")[0]["avg_price"]
                        loss_ratio = (price - avg_price) / avg_price
                        if loss_ratio <= max_sell_loss_ratio:
                            self.sell(coin, price, sell_amount)
                        else:
                            raise ValueError("Invalid strategy parameter. Choose either 'fixed', 'macd', or 'breakout_signal'")