class ParameterDict:
    def __init__(self):
        pass

    name2id = {
        "btc": "5",
        "eth": "29",
        "xrp": "83",
        "bch": "41",
        "qash": "50",
        "ltc": "847",
        "bat": "846",
    }

    resolution2id = {
        "1min": "60",
        "5min": "300",
        "15min": "900",
        "30min": "1800",
        "1hour": "3600",
    }

    side_list = [
        "buy",
        "sell",
    ]

    fiat_list = [
        "jpy",
    ]
