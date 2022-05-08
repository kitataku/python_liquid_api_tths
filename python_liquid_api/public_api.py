from .parameter_dict import ParameterDict
import requests
import json
import datetime
import pandas as pd
import warnings


class LiquidPublic:
    def __init__(self):
        self.end_point = "https://api.liquid.com/"
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
        url += "products/"

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
        url += "products/"

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

    def get_executions(self, currency_name, date, hour):
        """
        約定履歴を取得
        :param currency_name: 通貨名
        :param date: 日付(yyyymmdd)
        :param hour: 時間(hh)
        """
        def timestamp2datetime(timestamp):
            return datetime.datetime.fromtimestamp(float(timestamp))

        url_tmp = self.end_point
        url_tmp += "executions"

        query_tmp = None
        # 通貨名の不正チェック
        if currency_name in self.parameter_dict.name2id:
            query_tmp = "?product_id="
            query_tmp += self.parameter_dict.name2id[currency_name]
            query_tmp += "&limit=1000"
        else:
            raise ValueError("通貨名が不正です。")

        # 日付をUNIX時間に変換
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:8])
        hour = int(hour)

        target_timestamp = datetime.datetime(year, month, day, hour).timestamp()
        end_timestamp = target_timestamp + 60*60  # 開始時点のtimestampの1時間(3600秒)後

        # 出力用DataFrame
        out_df = pd.DataFrame(columns=["id", "quantity", "price", "taker_side", "created_at", "timestamp"])

        # 比較対象のtimestampが開始時点のtimestampの1時間(3600秒)後までLOOP
        while target_timestamp < end_timestamp:
            query = query_tmp + "&timestamp=" + str(target_timestamp)

            # URLにクエリを追加
            url = url_tmp + query

            # 送信
            req_result = requests.get(url).text
            parsed_data = json.loads(req_result)

            # 約定データが取得できなかった場合
            if len(parsed_data) == 0:
                if len(out_df) == 0:
                    # 出力用DataFrameがまだ作成されていない場合は処理を終了
                    return pd.DataFrame()
                else:
                    # 出力用DataFrameが作成されている場合は加工処理へ
                    break

            # DataFrameを作成
            df = pd.DataFrame(parsed_data)
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
