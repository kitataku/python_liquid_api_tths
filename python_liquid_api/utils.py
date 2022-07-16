# 定数
GOOD_CODE = "200"
UNKNOWN_ERROR_CONT = "不明なエラーです。"


def json_parse(request_result):
    """
    リクエスト結果のJSONデータをパースする。
    リクエストエラーがある場合は例外を起こす。
    """
    request_code = str(request_result.status_code)
    if request_code == GOOD_CODE:
        # JSONデータをパース
        return request_result.json()
    else:
        # エラーコードに対応する文章を取得
        if request_code in ERROR_CODES:
            error_contents = ERROR_CODES[request_code]
        else:
            error_contents = UNKNOWN_ERROR_CONT

        # エラーコードと対応する文章を出力
        message = "Error Code:" + request_code + " Contents:" + error_contents
        raise Exception(message)


def url_add_currency(url, currency_name):
    """
    URLに通貨IDを追加する
    """
    if currency_name in CURRENCY_ID:
        url += CURRENCY_ID[currency_name]
        return url
    else:
        raise ValueError("通貨名が不正です。")


def set_url(access_type, currency_name, resolution=None, max_data_num=1000):
    url = "https://api.liquid.com/"
    if access_type == "ohlc":
        # ローソク足
        # https://api.liquid.com/products/{product_id}/ohlc?resolution={resolution}
        url += "products/"
        url = url_add_currency(url, currency_name)
        url += "/ohlc?resolution="

        if resolution in CANDLE_TYPES:
            url += CANDLE_TYPES[resolution]
        else:
            raise ValueError("ローソク足のタイプが不正です。:", resolution)

    elif access_type == "book":
        # 板情報
        # https://api.liquid.com/products/{product_id}/price_levels?full=0
        url += "products/"
        url = url_add_currency(url, currency_name)
        url += "/price_levels?full=0"

    elif access_type == "executions":
        # 約定情報
        # https://api.liquid.com/executions?product_id={product_id}&limit={limit}&page={page}
        url += "executions" + "?product_id="
        url = url_add_currency(url, currency_name)
        url += "&limit=" + str(max_data_num)

    return url


# エラーコードと出力文章の対応
ERROR_CODES = {
    "404": "URLが存在しません。",
    "414": "URLが長すぎます。"
}

# 通貨略称と通貨IDの対応
CURRENCY_ID = {
    "btc": "5",
    "eth": "29",
    "xrp": "83",
    "bch": "41",
    "qash": "50",
    "ltc": "847",
    "bat": "846",
}

CANDLE_TYPES = {
    "1min": "60",
    "5min": "300",
    "15min": "900",
    "30min": "1800",
    "1hour": "3600",
}