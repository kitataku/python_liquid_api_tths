from .utils import json_parse, url_add_currency, set_url
import requests
import json
import datetime
import pandas as pd
import warnings


class LiquidPublic(object):
    @staticmethod
    def get_candlestick_raw(currency_name, candle_type):
        """
        ローソク足を取得して生データを出力
        :param currency_name: 通貨名
        :param candle_type: ローソク足範囲
        - 1min
        - 5min
        - 15min
        - 30min
        - 1hour
        :return: ローソク足Data
        - datetime: UNIX Timestamp
        - open
        - high
        - low
        - close
        - volume
        """
        # URLの設定
        set_url_params = {
            "access_type": "ohlc",
            "currency_name": currency_name,
            "resolution": candle_type
        }
        url = set_url(**set_url_params)

        # APIからローソク足を取得
        req_result = requests.get(url)
        raw_data = json_parse(req_result)["data"]

        return raw_data

    def get_candlestick(self, currency_name, date, candle_type, is_index_datetime=True):
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
        # ローソク足の生データを取得
        parsed_data = self.get_candlestick_raw(currency_name, candle_type)

        # DataFrameに変換
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

        if len(output_df) == 0:
            warnings.warn("指定日付が取得範囲外です。")

        return output_df

    @staticmethod
    def get_order_book_raw(currency_name):
        """
        板情報の生データを取得
        - buy_price_levels: 買値
        - sell_price_levels: 売値
        - timestamp: 取得日時
        """
        # URLの設定
        set_url_params = {
            "access_type": "book",
            "currency_name": currency_name,
        }
        url = set_url(**set_url_params)

        # 板情報の生データを取得
        req_result = requests.get(url)
        raw_data = json_parse(req_result)

        return raw_data

    def get_order_book(self, currency_name):
        """
        板情報を取得
        :param currency_name: 通貨名
        :return: 売値DataFrame, 買値DataFrame, datetime
        """
        # 板情報の生データを取得
        order_book_raw = self.get_order_book_raw(currency_name)

        # 売値
        bid_df = pd.DataFrame(
            data=order_book_raw["sell_price_levels"],
            columns=["bid_price", "bid_volume"]
        )

        # 買値
        ask_df = pd.DataFrame(
            data=order_book_raw["buy_price_levels"],
            columns=["ask_price", "ask_volume"]
        )

        # 板情報取得日時
        datetime_data = datetime.datetime.fromtimestamp(float(order_book_raw["timestamp"]))
        return bid_df, ask_df, datetime_data

    @staticmethod
    def get_executions_raw(currency_name, timestamp, max_data_num=1000, base_url=None):
        """
        約定履歴を取得
        :param currency_name: 通貨名
        :param timestamp: 取得対象timestamp
        :param max_data_num: 最大取得データ数
        :param base_url: 約定履歴を取得するURLのからtimestampを指定する部分を除いたURL
        """
        if base_url is None:
            # URLを設定
            set_url_params = {
                "access_type": "executions",
                "currency_name": currency_name,
                "max_data_num": max_data_num,
            }
            url_tmp = set_url(**set_url_params)
        else:
            url_tmp = base_url

        url = url_tmp + "&timestamp=" + str(timestamp)
        req_result = requests.get(url)
        raw_data = json_parse(req_result)
        return raw_data, url_tmp

    def get_executions(self, currency_name, date, hour):
        """
        約定履歴を取得
        :param currency_name: 通貨名
        :param date: 日付(yyyymmdd)
        :param hour: 時間(hh)
        """
        def timestamp2datetime(timestamp):
            return datetime.datetime.fromtimestamp(float(timestamp))

        # 取得対象のtimestampを取得
        target_timestamp = datetime.datetime.strptime(date+hour, "%Y%m%d%H").timestamp()
        end_timestamp = target_timestamp + 60*60  # 開始時点のtimestampの1時間(3600秒)後

        # 出力用DataFrame
        out_df = pd.DataFrame(columns=["id", "quantity", "price", "taker_side", "created_at", "timestamp"])

        url = None
        # 比較対象のtimestampが開始時点のtimestampの1時間(3600秒)後までLOOP
        while target_timestamp < end_timestamp:
            # 約定生データと基底URLを取得
            raw_data, url = self.get_executions_raw(currency_name, target_timestamp, base_url=url)

            # 約定データが取得できなかった場合
            if len(raw_data) == 0:
                if len(out_df) == 0:
                    # 出力用DataFrameがまだ作成されていない場合は処理を終了
                    return pd.DataFrame()
                else:
                    # 出力用DataFrameが作成されている場合は加工処理へ
                    break

            # DataFrameを作成
            df = pd.DataFrame(raw_data)
            merge_df = pd.merge(out_df, df, on="timestamp")

            # 約定データがすべて取得済の場合
            if len(merge_df) == len(df):
                if len(out_df) == 0:
                    # 出力用DataFrameがまだ作成されていない場合は処理を終了
                    return pd.DataFrame()
                else:
                    # 出力用DataFrameが作成されている場合は加工処理へ
                    break

            target_timestamp = df.tail(1)["timestamp"].values[0]  # 最後のレコードのtimestampを次の取得地点とする
            target_timestamp = float(target_timestamp)  # whileで比較するためにfloatに変換

            out_df = pd.concat([out_df, df], axis=0)

        # 出力用に加工
        out_df = out_df.loc[out_df["timestamp"] < str(end_timestamp)]  # 終了timestampより前のレコードのみ取得
        out_df["timestamp"] = out_df["timestamp"].apply(timestamp2datetime)  # UNIX時間を変換
        out_df = out_df.drop_duplicates(subset="id")  # idで重複削除
        out_df = out_df.reset_index(drop=True)  # indexを削除
        out_df = out_df.drop(["created_at", "id"], axis=1)  # 不要な列を削除

        return out_df
