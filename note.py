from python_liquid_api.public_api import LiquidPublic

a = LiquidPublic()

c_name = "btc"
c_type = "5min"
b = a.get_executions(c_name, "20220716", "17")

print(b)