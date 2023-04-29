import pyupbit
import jwt
import uuid
import hashlib
import requests
import datetime
from urllib.parse import urlencode

access_key = "RtNkYNkqltxtJbE9E9OfI2se4xlWDxxKRx5mrQhO"
secret_key = "FkougvxZA0nnVet6DdNNktj9vXSjpVnDixfe6sxz"
server_url = "https://api.upbit.com"

class UpbitAPI:
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key
        self.server_url = "https://api.upbit.com"
    def _request_headers(self, payload=None):
        if payload is None:
            payload = {}
        payload_str = urlencode(payload)
        m = hashlib.sha512()
        m.update(payload_str.encode('utf-8'))
        b64 = pyupbit.base64.b64encode(m.digest()).decode('utf-8')
        jwt_payload = {
            'access_key': self.access,
            'nonce': str(uuid.uuid4()),
            'query': payload_str
        }
        encoded_jwt = jwt.encode(jwt_payload, self.secret, algorithm='HS256').decode('utf-8')
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(encoded_jwt)
        }
    def _request_api(self, end_point, method='GET', params=None, payload=None):
        url = self.server_url + end_point
        headers = self._request_headers(payload)
        res = requests.request(method, url, params=params, headers=headers)
        try:
            if 'success' in res.json() and not res.json()['success']:
                raise Exception(res.json()['error']['message'])
            return res.json()
        except ValueError:
            raise ValueError('API Error')
    def get_ticker(self, markets):
        """
        마켓의 현재가를 얻어옵니다.
        :param markets: 마켓 코드의 배열
        :return: 호가 정보 딕셔너리
        """
        if not isinstance(markets, list):
            markets = [markets]
        query = {
            'markets': ','.join(markets)
        }
        return self._request_api('/v1/ticker', params=query)
    def buy_market_order(self, market, price):
        """
        시장가 매수 주문을 요청합니다.
        :param market: 마켓 코드(종목 코드)
        :param price: 주문 가격
        :return: 주문 정보 딕셔너리
        """
        query = {
            'market': market,
            'side': 'bid',
            'price': str(price),
            'ord_type': 'price',
        }
        return self._request_api('/v1/orders', method='POST', params=query)    
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
    def get_my_balance(currency):
        query = {
            'currency': currency,
        }
        query_string = urlencode(query).encode()
        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()
        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }
        jwt_token = jwt.encode(payload, secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}
        res = requests.get(server_url + "/v1/accounts", params=query, headers=headers)
        return res.json()
    def upbit_buy_order(ticker: str, price: float, volume: float):
        access_key = "RtNkYNkqltxtJbE9E9OfI2se4xlWDxxKRx5mrQhO"
        secret_key = "FkougvxZA0nnVet6DdNNktj9vXSjpVnDixfe6sxz"
        upbit = pyupbit.Upbit(access_key, secret_key)
        return upbit.buy_limit_order(ticker, price, volume)
        balance = pyupbit.get_my_balance()
        krw_balance = float(next(b for b in balance if b['currency'] == 'KRW')['balance'])
        print("KRW balance:", krw_balance)
        buy_order = upbit_buy_order("BTC-KRW", 40000000, 0.001)
        print("Buy order:", buy_order)
    def upbit_sell_order(ticker: str, price: float, volume: float):
        access_key = "RtNkYNkqltxtJbE9E9OfI2se4xlWDxxKRx5mrQhO"
        secret_key = "FkougvxZA0nnVet6DdNNktj9vXSjpVnDixfe6sxz"
        server_url = "https://api.upbit.com"
        payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        }
        jwt_token = jwt.encode(payload, secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}
    # 매도 주문 요청 생성
        query = {
            'market': ticker,
            'side': 'ask', # 판매 주문
            'volume': str(volume),
            'price': str(price),
            'ord_type': 'limit', # 지정가 주문
        }
        query_string = urlencode(query).encode()
        # 생성한 요청 정보로 매도 주문 요청 실행
        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()
        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }
        jwt_token = jwt.encode(payload, secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}
        res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
        return res.json()
    if __name__ == "__main__":
        print("Your balance: ", get_my_balance("KRW"))
        print("Buy order: ", upbit_buy_order("KRW-BTC", 0.001, 40000000))
