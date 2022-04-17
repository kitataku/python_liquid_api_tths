import jwt
import json
import requests
from datetime import datetime
import warnings

from .parameter_dict import ParameterDict


class LiquidPrivate:
    def __init__(self, token_id, secret_key):
        """
        :param token_id:
        :param secret_key:
        """
        self.token_id = token_id
        self.secret_key = secret_key

        self.endpoint = "https://api.liquid.com/"
        self.parameter_dict = ParameterDict()

    def __make_header(self, path, query=""):
        timestamp = datetime.now().timestamp()
        path += query

        payload_data = {
            "path": path,
            "nonce": timestamp,
            "token_id": self.token_id
        }
        signature = jwt.encode(payload_data, self.secret_key, algorithm="HS256")
        header = {
            "X-Quoine-API-Version": "2",
            "X-Quoine-Auth": signature,
            "Content-Type": "application/json"
        }

        return path, header

    def __check_and_trans_params(self, currency_name, side, amount, price):
        currency_id = None

        if currency_name is not None:
            try:
                currency_id = self.parameter_dict.name2id[currency_name]
            except KeyError:
                raise ValueError("通貨名が不正です。")

        if side is not None:
            if side not in self.parameter_dict.side_list:
                raise ValueError("注文にはbuyもしくはsellを指定してください。")

        amount = float(amount)
        price = float(price)

        return currency_id, amount, price

    def create_order(self, currency_name, side, amount, price=0.0, order_type="limit"):
        """
        注文
        :param currency_name: 通貨名
        :param side: 売/買
        - sell: 売り注文
        - buy: 買い注文
        :param amount: 注文量
        :param price: 注文単価
        :param order_type: 注文タイプ
        - limit: 指値注文
        - market: 成行注文
        :return:
        """
        url = self.endpoint + "orders/"
        currency_id, amount, price = self.__check_and_trans_params(
            currency_name=currency_name,
            side=side,
            amount=amount,
            price=price
        )

        # ヘッダ情報作成
        url, header = self.__make_header(path=url)

        # 注文データ
        send_data = {
            "order": {
                "order_type": order_type,
                "product_id": currency_id,
                "side": side,
                "quantity": amount,
                "price": price,
            }
        }

        # 送信データ作成
        json_data = json.dumps(send_data)
        res = requests.post(url=url, headers=header, data=json_data)

        parsed_data = json.loads(res.text)
        create_datetime = datetime.fromtimestamp(parsed_data["created_at"])
        create_datetime = datetime.strftime(create_datetime, "%Y/%m/%d %H:%M:%S")

        update_datetime = datetime.fromtimestamp(parsed_data["updated_at"])
        update_datetime = datetime.strftime(update_datetime, "%Y/%m/%d %H:%M:%S")

        output = {
            "transaction_id": str(parsed_data["id"]),
            "order_type": parsed_data["order_type"],
            "quantity": float(parsed_data["quantity"]),
            "price": float(parsed_data["price"]),
            "side": parsed_data["side"],
            "created_at": create_datetime,
            "updated_at": update_datetime,
            "currency": parsed_data["currency_pair_code"][:-3]  # 取引通貨のみ取得（文字列からJPYを除く）
        }

        return output

    def get_order_info(self, limit_num=None):
        url = self.endpoint + "orders"
        query = None

        # 取得件数を指定した場合はクエリを設定
        if limit_num is not None:
            query = "?limit=" + str(limit_num)

        # ヘッダ情報作成
        url, header = self.__make_header(path=url, query=query)
        # データ送信
        res = requests.get(url=url, headers=header)

        if res.status_code != 200:
            print("注文情報の取得に失敗しました。")
            return None

        parsed_data = json.loads(res.text)["models"]
        output_list = []
        for data in parsed_data:
            create_datetime = datetime.fromtimestamp(data["created_at"])
            create_datetime = datetime.strftime(create_datetime, "%Y/%m/%d %H:%M:%S")

            update_datetime = datetime.fromtimestamp(data["updated_at"])
            update_datetime = datetime.strftime(update_datetime, "%Y/%m/%d %H:%M:%S")

            # 出力データ作成
            output_dict = {
                "transaction_id": str(data["id"]),
                "order_type": data["order_type"],
                "price": float(data["price"]),
                "quantity": float(data["quantity"]),
                "filled_quantity": float(data["filled_quantity"]),  # 約定済の量
                "side": data["side"],
                "created_at": create_datetime,
                "updated_at": update_datetime,
                "currency": data["currency_pair_code"][:-3]  # 取引通貨のみ取得（文字列からJPYを除く）
            }

            output_list.append(output_dict)

        return output_list

    def cancel_order(self, order_id):
        url = self.endpoint + "orders/" + order_id + "/cancel"
        # ヘッダ情報作成
        header = self.__make_header(path=url)
        # データ送信
        res = requests.put(url=url, headers=header)

        if res.status_code == 404:
            print("対象の取引IDが存在しません。取引ID:", order_id)
        elif res.status_code == 200:
            print("注文がキャンセルされました。取引ID:", order_id)

    def get_fiat_info(self):
        """
        日本円残高取得
        :return:
        - balanced: 利用可能残高
        - reserved: ロック中残高
        """
        warnings.warn("廃止予定のメソッドです。get_asset_info(asset='jpy')を使用してください。", category=FutureWarning)
        url = self.endpoint + "fiat_accounts"
        # ヘッダ情報作成
        url, header = self.__make_header(path=url)
        # データ送信
        res = requests.get(url=url, headers=header)
        parsed = json.loads(res.text)[0]

        balance = parsed["balance"]  # 日本円残高
        reserved = parsed["reserved_balance"]  # ロック中
        return balance, reserved

    def get_crypto_info(self, currency="btc"):
        warnings.warn("廃止予定のメソッドです。get_asset_info(asset)を使用してください。", category=FutureWarning)
        url = self.endpoint + "crypto_accounts"
        # ヘッダ情報作成
        url, header = self.__make_header(path=url)
        # データ送信
        res = requests.get(url=url, headers=header)
        parsed = json.loads(res.text)

        currency = currency.upper()
        data = None
        # 引数で与えた通貨の情報を取得
        for p in parsed:
            if p["currency"] == currency:
                data = p
                break

        balance = data["balance"]  # 利用可能残高
        reserved = data["reserved_balance"]  # ロック中残高

        return balance, reserved

    def get_asset_info(self, asset):
        url = self.endpoint
        # 日本円を指定した場合
        if asset in self.parameter_dict.fiat_list:
            url += "fiat_accounts"
        # 暗号資産を指定した場合
        elif asset in self.parameter_dict.name2id:
            url += "crypto_accounts"
        else:
            raise Exception("通貨名が不正です。")

        # ヘッダ情報作成
        url, header = self.__make_header(path=url)
        # データ送信
        res = requests.get(url=url, headers=header)
        parsed = json.loads(res.text)
        asset = asset.upper()

        data = None
        # 引数で与えた通貨の情報を取得
        for p in parsed:
            if p["currency"] == asset:
                data = p
                break

        balance = data["balance"]  # 利用可能残高
        reserved = data["reserved_balance"]  # ロック中残高

        return balance, reserved
