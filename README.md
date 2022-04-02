# python_liquid_api

## API概要

このライブラリはLiquid APIのPrivate APIとPublic APIをPythonで扱うものです。

## ダウンロード

pip install python-liquid-api-tths

## Public API

Public APIを使うにはLiquidPublicをインスタンス化します。

```python
from python_liquid_api.public_api import LiquidPublic

pub = LiquidPublic()
```

### get_candlestick

このメソッドを使用することでOHLCVデータを取得することができます。

#### 引数

- currency_name: 取得対象の通貨名を指定します。指定できる値は次の通りです。
  - btc
  - eth
  - xrp
  - bch
  - qash
  - ltc
  - bat

- date: 取得対象の日付を指定します。フォーマットはyyyymmddの文字列です。
- candle_type: 取得するローソク足のタイプを指定します。指定できる値は次の文字列です。
  - 1min: 1分足を取得します
  - 5min: 5分足を取得します
  - 15min: 15分足を取得します
  - 30min: 30分足を取得します
  - 1hour: 1時間足を取得します