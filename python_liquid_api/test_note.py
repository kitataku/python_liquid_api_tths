from python_liquid_api import public_api
from python_liquid_api import private_api
import os
import pandas as pd

pd.set_option("display.max_columns", None)
#a = public_api.LiquidPublic()
pri = private_api.LiquidPrivate(token_id="xxxxxx", secret_key="xxxxxxxxxxxx")
#r = pri.create_order(currency_name="qash", side="buy", amount=1.0, price=7.00)
#r = pri.cancel_order("xxxxxxx)
r = pri.get_order_info(limit_num=50)
df = pd.DataFrame(r)

print(df[df["filled_quantity"] == 0.0])
