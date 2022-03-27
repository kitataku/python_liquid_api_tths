from python_liquid_api import public_api
from python_liquid_api import private_api
import os
import pandas as pd

pd.set_option("display.max_columns", None)
#a = public_api.LiquidPublic()
pri = private_api.LiquidPrivate(token_id=os.environ["id"], secret_key=os.environ["key"])
r = pri.create_order(currency_name="qash", side="buy", amount=1.0, order_type="market")
#r = pri.cancel_order("xxxxxxx)
#r = pri.get_order_info(limit_num=50)
#df = pd.DataFrame(r)

#print(df[df["filled_quantity"] == 0.0])

#balanced, reserved = pri.get_fiat_info()
#print(balanced, type(balanced))
#print(reserved, type(reserved))

balanced, reserved = pri.get_crypto_info(currency="BTC")
print(balanced, type(balanced))
print(reserved, type(reserved))