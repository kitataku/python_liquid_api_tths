# 更新履歴
## 0.3.0
現物取引注文をするメソッド(create_order)で逆指値注文ができるようになりました。  
もともとorder_typeにstopを指定すれば逆指値注文することはできていましたが、動作確認をした上で引数に指定可能であることを明記しました。

## 0.3.2
注文をキャンセルするメソッド(cancel_order)を使用したときにエラーが出ていたので修正しました。

## 0.4.0
public APIにおいて生データを取得できるようにしました。
- get_candlestick_raw: ローソク足
- get_order_book_raw: 板情報
- get_executions_raw: 約定履歴