# python_liquid_api_tths
## API概要
このライブラリはLiquid APIのPrivate APIとPublic APIをPythonで扱うものです。

PyPI
https://pypi.org/project/python-liquid-api-tths/

## インストール
```shell
pip install python-liquid-api-tths
```

## Public API
Public APIを使うにはLiquidPublicをインスタンス化します。引数は必要ありません。

```python
from python_liquid_api.public_api import LiquidPublic
pub = LiquidPublic()
```

### get_candlestick
このメソッドを使用することでOHLCVデータを取得することができます。
```python
from python_liquid_api.public_api import LiquidPublic
pub = LiquidPublic()
ohlc = pub.get_candlestick(currency_name, date, candle_type)
```

#### 引数
- **currency_name**: 取得対象の通貨名を指定します。指定できる値は次の通りです。
  - btc: ビットコイン
  - eth: イーサリアム
  - xrp: リップル
  - bch: ビットコインキャッシュ
  - qash: キャッシュ
  - ltc: ライトコイン
  - bat: ベーシックアテンショントークン
- **date**: 取得対象の日付を指定します。フォーマットはyyyymmddの文字列です。
- **candle_type**: 取得するローソク足のタイプを指定します。指定できる値は次の文字列です。
  - 1min: 1分足を取得します
  - 5min: 5分足を取得します
  - 15min: 15分足を取得します
  - 30min: 30分足を取得します
  - 1hour: 1時間足を取得します

#### 返り値
- **output_df**: pandas.DataFrame型のOHLCVが格納されたデータです。列は次の通りです。
  - datetime: datatime型の日時(yyyy-mm-dd hh:mm:ss)
  - open: 始値
  - high: 高値
  - low: 低値
  - close: 終値
  - volume: 出来高

#### 例外
- **通貨名が不正です。**: 引数のcurrency_nameに指定できる通貨名以外を指定した場合に発生します。
- **ローソク足のタイプが不正です。**: 引数のcandle_typeに指定できる値以外を指定した場合に発生します。

### get_order_book
このメソッドを使用することでいた情報を取得することができます。
```python
from python_liquid_api.public_api import LiquidPublic
pub = LiquidPublic()
ohlc = pub.get_order_book(currency_name)
```

#### 引数
- **currency_name**: 取得対象の通貨名を指定します。指定できる値は次の通りです。
  - btc: ビットコイン
  - eth: イーサリアム
  - xrp: リップル
  - bch: ビットコインキャッシュ
  - qash: キャッシュ
  - ltc: ライトコイン
  - bat: ベーシックアテンショントークン

#### 返り値
- **bid_df**: pandas.DataFrame型の売値データです。
- **ask_df**: pandas.DataFrame型の買値データです。
- **datetime_data**: datetime型の板情報取得日時です。

#### 例外
- **通貨名が不正です。**: 引数のcurrency_nameに指定できる通貨名以外を指定した場合に発生します。

## Private API
Private APIを使うにはLiquidPrivateをインスタンス化します。

```python
from python_liquid_api.private_api import LiquidPrivate
pri = LiquidPrivate(token_id, secret_key)
```

#### 引数
- **token_id**: トークンIDです。
- **secret_key**: APIトークン秘密鍵です。

### create_order
このメソッドを使うことで現物取引の取引注文を出すことができます。
```python
from python_liquid_api.private_api import LiquidPrivate
pri = LiquidPrivate(token_id, secret_key)
order_info = pri.create_order(currency_name, side, amount, price=0.0, order_type="limit")
```

#### 引数
- **currency_name**: 取得対象の通貨名を指定します。指定できる値は次の通りです。
  - btc: ビットコイン
  - eth: イーサリアム
  - xrp: リップル
  - bch: ビットコインキャッシュ
  - qash: キャッシュ
  - ltc: ライトコイン
  - bat: ベーシックアテンショントークン
- **side**: 売買の指定をします。指定できる値は次の通りです。
  - sell: 売り注文
  - buy: 買い注文
- **amount**: 注文量を指定します。
- **price**: 注文単価を指定します。
- **order_type**: 注文方法を指定します。指定できる値は次の通りです。
  - limit: 指値注文
  - market: 成行注文

#### 返り値
- **output**: 辞書型の注文情報です。
  - transaction_id: 取引ID
  - order_type: 注文方法(limit/market)
  - quantity: 注文量
  - price: 取引単価
  - side: 売買(sell/buy)
  - created_at: 登録日時
  - updated_at: 更新日時
  - currency: 取引通貨名

#### 例外
- **通貨名が不正です。**: 引数のcurrency_nameに指定できる通貨名以外を指定した場合に発生します。
- **注文にはbuyもしくはsellを指定してください。**: 引数のsideに指定できる値以外を指定した場合に発生します。

### cancel_order
このメソッドをを使うことで注文をキャンセルすることができます。
```python
from python_liquid_api.private_api import LiquidPrivate
pri = LiquidPrivate(token_id, secret_key)
pri.cancel_order(order_id)
```

#### 引数
- order_id: キャンセル対象の取引IDを指定します。

### get_asset_info
このメソッドを使うことで資産の残高を取得することができます。
```python
from python_liquid_api.private_api import LiquidPrivate
pri = LiquidPrivate(token_id, secret_key)
pri.get_fiat_info()
```
#### 例外
- **通貨名が不正です。**: 引数のcurrency_nameに指定できる通貨名以外を指定した場合に発生します。

### get_fiat_info
**! 廃止予定のメソッド**
get_asset_infoを使ってください。

このメソッドを使うことで日本円の残高を取得することができます。
```python
from python_liquid_api.private_api import LiquidPrivate
pri = LiquidPrivate(token_id, secret_key)
pri.get_fiat_info(asset)
```
#### 引数
- **currency_name**: 取得対象の通貨名を指定します。指定できる値は次の通りです。
  - btc: ビットコイン
  - eth: イーサリアム
  - xrp: リップル
  - bch: ビットコインキャッシュ
  - qash: キャッシュ
  - ltc: ライトコイン
  - bat: ベーシックアテンショントークン
  - jpy: 日本円

#### 返り値
- **balance**: 利用可能残高
- **reserved**: ロック中残高

#### 返り値
- **balance**: 利用可能残高です。
- **reserved**: ロック中残高です。

### get_crypto_info
**! 廃止予定のメソッド**
get_asset_infoを使ってください。

このメソッドを使うことで暗号資産の残高を取得することができます。
```python
from python_liquid_api.private_api import LiquidPrivate
pri = LiquidPrivate(token_id, secret_key)
pri.get_crypto_info(currency="btc")
```

#### 引数
- **currency_name**: 取得対象の通貨名を指定します。指定できる値は次の通りです。
  - btc: ビットコイン
  - eth: イーサリアム
  - xrp: リップル
  - bch: ビットコインキャッシュ
  - qash: キャッシュ
  - ltc: ライトコイン
  - bat: ベーシックアテンショントークン

#### 返り値
- **balance**: 利用可能残高です。
- **reserved**: ロック中残高です。
