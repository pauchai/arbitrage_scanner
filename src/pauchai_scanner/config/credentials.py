import os

config_credentials = {
    'binance': {
        'credentials': {
            'apiKey': os.getenv("BINANCE_API_KEY"),
            'secret': os.getenv("BINANCE_API_SECRET")
        }
    },
    'bybit': {
        'credentials': {
            'apiKey': os.getenv("BYBIT_API_KEY"),
            'secret': os.getenv("BYBIT_API_SECRET")
        }
    },
    'bingx': {
        'credentials': {
            'apiKey': os.getenv("BINGX_API_KEY"),
            'secret': os.getenv("BINGX_API_SECRET")
        }
    },
    'kucoin': {
        'credentials': {
            'apiKey': os.getenv("KUCOIN_API_KEY"),
            'secret': os.getenv("KUCOIN_API_SECRET"),
            'password': os.getenv("KUCOIN_API_PASSPHRASE")
        }
    },
    'okx': {
        'credentials': {
            'apiKey': os.getenv("OKX_API_KEY"),
            'secret': os.getenv("OKX_API_SECRET"),
            'password': os.getenv("OKX_API_PASSPHRASE")
        }
    },
    'mexc': {
        'credentials': {
            'apiKey': os.getenv("MEXC_API_KEY"),
            'secret': os.getenv("MEXC_API_SECRET")
        }
    },
    'htx': {
        'credentials': {
            'apiKey': os.getenv("HTX_API_KEY"),
            'secret': os.getenv("HTX_API_SECRET"),
            
        }
    },
    'bitmart': {
        'credentials': {
            'apiKey': os.getenv("BITMART_API_KEY"),
            'secret': os.getenv("BITMART_API_SECRET")
        }
    }
}
