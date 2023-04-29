import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests
import pyupbit
import datetime

access_key = "RtNkYNkqltxtJbE9E9OfI2se4xlWDxxKRx5mrQhO"
secret_key = "FkougvxZA0nnVet6DdNNktj9vXSjpVnDixfe6sxz"
server_url = "https://api.upbit.com"

class UpbitAPI:
    
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key
        self.server_url = 'https://api.upbit.com'
    
    def get_server_time(self):
        url = self.server_url + '/v1/server_time'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()['server_time']
        except Exception as e:
            print(e)
            return None
    
    def get_accounts(self):
        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4())
        }

        jwt_token = jwt.encode(payload, self.secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.get(self.server_url + '/v1/accounts', headers=headers)
        if res.status_code == 200:
            return res.json()
        else:
            return None
    
    def get_balance(self, currency):
        url = self.server_url + '/v1/accounts'
        try:
            headers = self.get_authentication_headers('GET', url)

            querystring = urlencode({'currency': currency})
            res = requests.get(url + '?' + querystring, headers=headers)
            if res.status_code == 200:
                return res.json()[0]
            else:
                return None
        except Exception as e:
            print(str(e))
            return None
            
    def get_ticker(self, markets):
        url = self.server_url + f"/v1/ticker?markets={markets}"
        try:
            querystring = urlencode({'markets': markets})
            response = requests.get(url, params=querystring)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(e)
            return None
    
    def get_authentication_headers(self, method, url):
        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
        }

        if method == 'GET':
            query_string = urlencode(payload)
            m = hashlib.sha512()
            m.update(query_string.encode())
            query_hash = m.hexdigest()
            url_path = url + '?' + query_string

        elif method == 'POST':
            m = hashlib.sha512()
            m.update(payload.encode())
            query_hash = m.hexdigest()
            url_path = url

        payload['query_hash'] = query_hash
        payload['query_hash_alg'] = 'SHA512'
        jwt_token = jwt.encode(payload, self.secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}
        return headers
    
    def post_order(self, market, side, volume, price, ord_type='limit'):
        query = {
            'market': market,
            'side': side,
            'volume': volume,
            'price': price,
            'ord_type': ord_type,
        }
        url = self.server_url + '/v1/orders'
        headers = self.get_authentication_headers('POST', url)
        res = requests.post(url, headers=headers, json=query)
        if res.status_code == 201:
            return res.json()['uuid']
        else:
            return None
        
    def delete_order(self, uuid):
        url = self.server_url + f'/v1/order{uuid}'
        headers = self.get_authentication_headers('DELETE', url)
        res = requests.delete(url, headers=headers)
        if res.status_code == 200:
            return True
        else:
            return False
        
    def get_orderbook(self, market, count):
        url = self.server_url + f"/v1/orderbook?markets={market}&count={count}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(e)
            return None
    def get_trade(self, market, count):
        url = self.server_url + f"/v1/trades/ticks?market={market}&count={count}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(e)
            return None
    def get_candles(self, market, time_unit, count, to=None):
        url = self.server_url + f"/v1/candles/{time_unit}?market={market}&count={count}"
        if to is not None:
            url += f"&to={to}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(e)
            return None
    def get_daily_candles(self, market, to=None):
        url = self.server_url + f"/v1/candles/days?market={market}"
        if to is not None:
            url += f"&to={to}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(e)
            return None
    def get_minutes_candles(self, market, minutes, count, to=None):
        url = self.server_url + f"/v1/candles/minutes/{minutes}?market={market}&count={count}"
        if to is not None:
            url += f"&to={to}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(e)
            return None
    def get_order_status(self, market, order_id):
        url = self.server_url + f"/v1/order/detail?market={market}&order_id={order_id}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(e)
            return None
    def get_balance(self):
        url = self.server_url + "/v1/wallet/balance"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(e)
            return None
    def place_order(self, market, side, price, size, type):
        url = self.server_url + "/v1/order"
        data = {
            "market": market,
            "side": side,
            "price": price,
            "size": size,
            "type": type
        }
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(e)
            return None
    def cancel_order(self, market, order_id):
        url = self.server_url + "/v1/order"
        data = {
            "market": market,
            "order_id": order_id
        }
        try:
            response = requests.delete(url, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(e)
            return None
        
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
        # Place buy limit order
        buy_result = upbit.buy_limit_order(ticker, price, volume)
        print("Buy order:", buy_result)
        # Get KRW balance
        balance = pyupbit.get_my_balance()
        krw_balance = next(filter(lambda x: x["currency"]=="KRW", balance), None)
        print("Your balance:", balance)
        # Place limit buy order for Bitcoin
        if krw_balance is not None and float(krw_balance["balance"]) > 40000000:
            upbit_buy_order("BTC-KRW", 40000000, 0.001)
        else:
            print("Error: Insufficient KRW balance")

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
