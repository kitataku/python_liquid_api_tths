from .parameter_dict import ParameterDict
import requests
import json
import datetime
import pandas as pd
import warnings


class LiquidPublic:
    def __init__(self):
        self.end_point = "https://api.liquid.com/products/"
        self.parameter_dict = ParameterDict()

    def get_candlestick(self, currency_name, date, candle_type, is_index_datetime=False):
        """
        ローソク足を取得
        :param currency_name: 通貨名
        :param date: 取得対象日付
        :param candle_type: ローソク足範囲
        - 1min
        - 5min
        - 15min
        - 30min
        - 1hour
        :param is_index_datetime: indexにdatetimeを設定
        :return: ローソク足DataFrame
        - datetime: yyyy-mm-dd hh:mm:ss
        - open
        - high
        - low
        - close
        - volume
        """
        url = self.end_point

        # 通貨名の不正チェック
        if currency_name in self.parameter_dict.name2id:
            url += self.parameter_dict.name2id[currency_name]
        else:
            raise ValueError("通貨名が不正です。")
        url += "/ohlc"

        # ローソクタイプの不正チェック
        if candle_type in self.parameter_dict.resolution2id:
            # URLにresolutionを付与
            second = self.parameter_dict.resolution2id[candle_type]
            query = "?resolution=" + second + "&limit=800"
        else:
            raise ValueError("ローソク足のタイプが不正です。")

        url += query
        req_result = requests.get(url).text
        parsed_data = json.loads(req_result)["data"]

        output_df = pd.DataFrame(data=parsed_data, columns=["datetime", "open", "high", "low", "close", "volume"])
        output_df["datetime"] = output_df["datetime"].apply(datetime.datetime.fromtimestamp)

        # 引数のdateをdatetime型に変換
        target_date = datetime.datetime.strptime(date, "%Y%m%d")
        target_date_next = target_date + datetime.timedelta(days=1)

        # 引数で指定したデータを取得
        output_df = output_df.loc[(output_df["datetime"] >= target_date) & (output_df["datetime"] < target_date_next)]
        output_df = output_df.reset_index(drop=True)

        if is_index_datetime:
            # indexにdatetimeを設定
            output_df.index = output_df["datetime"]
            # datetime列を削除
            output_df = output_df.drop("datetime", axis=1)
        else:
            warning_str = "indexが連番になっています。将来indexはdatetimeに変更されます。\n"
            warning_str += "indexをdatetimeにする場合は引数にis_index_datetime=Trueを設定してください。"
            warnings.warn(warning_str, category=FutureWarning)

        if len(output_df) == 0:
            warnings.warn("指定日付が取得範囲外です。")

        return output_df

    def get_order_book(self, currency_name):
        """
        板情報を取得
        :param currency_name: 通貨名
        :return: 売値DataFrame, 買値DataFrame, datetime
        """
        url = self.end_point
        # 通貨名の不正チェック
        if currency_name in self.parameter_dict.name2id:
            url += self.parameter_dict.name2id[currency_name]
        else:
            raise ValueError("通貨名が不正です。")
        url += "/price_levels"
        query = "?full=0"
        url += query
        req_result = requests.get(url).text
        parsed_data = json.loads(req_result)

        # 売値
        bid_df = pd.DataFrame(data=parsed_data["sell_price_levels"], columns=["bid_price", "bid_volume"])

        # 買値
        ask_df = pd.DataFrame(data=parsed_data["buy_price_levels"], columns=["ask_price", "ask_volume"])

        # 板情報取得日時
        datetime_data = datetime.datetime.fromtimestamp(float(parsed_data["timestamp"]))
        return bid_df, ask_df, datetime_data
