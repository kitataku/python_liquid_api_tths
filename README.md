# python_liquid_api_tths
[![Downloads](https://static.pepy.tech/personalized-badge/python-liquid-api-tths?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/python-liquid-api-tths)
## API概要
このライブラリはLiquid APIのPrivate APIとPublic APIをPythonで扱うものです。

PyPI
https://pypi.org/project/python-liquid-api-tths/

## インストール
インストールにはコンソールで次のコマンドを実行します。
```shell
pip install python-liquid-api-tths
```

## 目次
1. [Public API](#public)  
   1-1. [ローソク足(OHLCV)を取得](#get_candlestick)  
   1-2. [板情報の取得](#get_order_book)  
   1-3. [約定データの取得](#get_execution)
2. [Private API](#private)  
   2-1. [注文](#order)  
   2-2. [注文のキャンセル](#order_cancel)  
   2-3. [資産残高の取得](#get_asset)  
   2-4. [日本円残高の取得（廃止予定メソッド）](#get_fiat)  
   2-5. [暗号資産残高の取得（廃止予定メソッド）](#get_crypto)  

## 1. <a id="public">Public API</a>

Public APIを使うにはLiquidPublicをインスタンス化します。引数は必要ありません。

```python
from python_liquid_api.public_api import LiquidPublic
pub = LiquidPublic()
```

### 1-1. <a id="get_candlestick">ローソク足(OHLCV)を取得</a>
ローソク足（OHLCVデータ）を取得するにはget_candlestickを使用します。

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
  - 1min: 1分足を取得
  - 5min: 5分足を取得
  - 15min: 15分足を取得
  - 30min: 30分足を取得
  - 1hour: 1時間足を取得
- **is_index_datetime**: indexにdatetimeを設定する

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

### 1-2. <a id="get_order_book">板情報の取得</a>
板情報を取得するにはget_order_bookを使用します。

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
- **bid_df**: pandas.DataFrame型の売値データ
- **ask_df**: pandas.DataFrame型の買値データ
- **datetime_data**: datetime型の板情報取得日時

#### 例外
- **通貨名が不正です。**: 引数のcurrency_nameに指定できる通貨名以外を指定した場合に発生します。

### 1-3. <a id="get_execution">約定情報の取得</a>
約定情報を取得するにはget_executionsを使用します。

```python
from python_liquid_api.public_api import LiquidPublic
pub = LiquidPublic()
execution_df = pub.get_executions(currency_name, date, hour)
```

#### 引数
- **currency_name**: 取得対象の通貨名。指定できる値は次の通りです。
  - btc: ビットコイン
  - eth: イーサリアム
  - xrp: リップル
  - bch: ビットコインキャッシュ
  - qash: キャッシュ
  - ltc: ライトコイン
  - bat: ベーシックアテンショントークン
- **date**: 取得対象の日付。フォーマットはyyyymmddの文字列
- **hour**: 取得対象の時間。フォーマットはhhの文字列

#### 返り値
- **out_df**: pandas.DataFrame型の約定データ
  - quantity: 取引量
  - price: 取引価格
  - taker_size: taker側のside(buy/sell)
  - timestamp: 取引された時刻


## 2. <a id="private">Private API</a>
Private APIを使うにはLiquidPrivateをインスタンス化します。

```python
from python_liquid_api.private_api import LiquidPrivate
pri = LiquidPrivate(token_id, secret_key)
```

#### 引数
- **token_id**: トークンID
- **secret_key**: APIトークン秘密鍵

### 2-1. <a id="order">注文</a>
現物取引の注文を出すにはcreate_orderを使用します。

```python
from python_liquid_api.private_api import LiquidPrivate
pri = LiquidPrivate(token_id, secret_key)
order_info = pri.create_order(currency_name, side, amount, price=0.0, order_type="limit")
```

#### 引数
- **currency_name**: 取得対象の通貨名。指定できる値は次の通りです。
  - btc: ビットコイン
  - eth: イーサリアム
  - xrp: リップル
  - bch: ビットコインキャッシュ
  - qash: キャッシュ
  - ltc: ライトコイン
  - bat: ベーシックアテンショントークン
- **side**: 売買の指定。指定できる値は次の通りです。
  - sell: 売り注文
  - buy: 買い注文
- **amount**: 注文量
- **price**: 注文単価
- **order_type**: 注文方法。指定できる値は次の通りです。
  - limit: 指値注文
  - market: 成行注文
  - stop: 逆指値注文

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

### 2-2. <a id="order_cancel">注文のキャンセル</a>
注文をキャンセルするにはcancel_orderを使用します。

```python
from python_liquid_api.private_api import LiquidPrivate
pri = LiquidPrivate(token_id, secret_key)
pri.cancel_order(order_id)
```

#### 引数
- order_id: キャンセル対象の取引ID


### 2-3. <a id="get_asset">資産残高の取得</a>
資産残高の取得をするにはget_asset_infoを使用します。

```python
from python_liquid_api.private_api import LiquidPrivate
pri = LiquidPrivate(token_id, secret_key)
pri.get_asset_info(asset)
```
#### 引数
- **asset**:  取得対象資産
  - jpy: 日本円
  - btc: ビットコイン
  - eth: イーサリアム
  - xrp: リップル
  - bch: ビットコインキャッシュ
  - qash: キャッシュ
  - ltc: ライトコイン
  - bat: ベーシックアテンショントークン

#### 例外
- **通貨名が不正です。**: 引数のcurrency_nameに指定できる通貨名以外を指定した場合に発生します。


### 2-4. <a id="get_fiat">日本円残高の取得</a>
**! 廃止予定のメソッド get_asset_infoを使ってください。**

日本円残高を取得するにはget_fiat_infoを使用します。

```python
from python_liquid_api.private_api import LiquidPrivate
pri = LiquidPrivate(token_id, secret_key)
pri.get_fiat_info()
```
#### 返り値
- **balance**: 利用可能残高
- **reserved**: ロック中残高

#### 返り値
- **balance**: 利用可能残高
- **reserved**: ロック中残高



### 2-5. <a id="get_crypto">暗号資産残高の取得</a>
**! 廃止予定のメソッド get_asset_infoを使ってください。**
暗号資産残高を取得するにはget_crypto_infoを使用します。

```python
from python_liquid_api.private_api import LiquidPrivate
pri = LiquidPrivate(token_id, secret_key)
pri.get_crypto_info(currency="btc")
```

#### 引数
- **currency_name**: 取得対象の通貨名
  - btc: ビットコイン
  - eth: イーサリアム
  - xrp: リップル
  - bch: ビットコインキャッシュ
  - qash: キャッシュ
  - ltc: ライトコイン
  - bat: ベーシックアテンショントークン

#### 返り値
- **balance**: 利用可能残高
- **reserved**: ロック中残高
