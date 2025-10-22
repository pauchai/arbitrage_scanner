import os
import argparse

config = {
    'binance': {
        'enabled': True,
        'ccxt': {
            'testnet': False,
            'enableRateLimit': True
        },
        'custom': {
            'url_templates': {
                'spot': "https://www.binance.com/en/trade/{base_currency}_{quoted_currency}?type=spot"
            }
        }
    },
    'bybit': {
        'enabled': True,
        'ccxt': {
            'testnet': False,
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'}
        },
        'custom': {
            'url_templates': {
                'spot': "https://www.bybit.com/trade/spot/{base_currency}/{quoted_currency}"
            }
        }
    },
    'bingx': {
        'enabled': True,
        'ccxt': {
            'testnet': False,
            'enableRateLimit': True
        },
        'custom': {
            'url_templates': {
                'spot': "https://bingx.com/en/spot/{base_currency}{quoted_currency}/"
            }
        }
    },
    'kucoin': {
        'enabled': True,
        'ccxt': {
            'testnet': False,
            'enableRateLimit': True
        },
        'custom': {
            'url_templates': {
                'spot': "https://www.kucoin.com/trade/{base_currency}-{quoted_currency}"
            }
        }
    },
    'okx': {
        'enabled': False ,  # временно отключена из-за проблем с API
        'ccxt': {
            'testnet': False,
            'enableRateLimit': True
        },
        'custom': {
            'url_templates': {  
                'spot': "https://www.okx.com/trade/{base_currency}-{quoted_currency}"
            }
        }
    },
    'mexc': {
        'enabled': True,# временно отключена нет API ключей
        'ccxt': {
            'testnet': False,
            'enableRateLimit': True
        },
        'custom': {
            'url_templates': {
                'spot': "https://www.mexc.com/exchange/{base_currency}_{quoted_currency}"
            }
        }
    },
    'htx': {
        'enabled': True,# временно отключена нет API ключей
        'ccxt': {
            'testnet': False,
            'enableRateLimit': True
        },
        'custom': {
            'url_templates': {
                'spot': "https://www.hathor.exchange/trade/{base_currency}-{quoted_currency}"
            }
        }
    },
    "bitmart": {
        'enabled': True,# временно отключена нет API ключей
        'ccxt': {
            'testnet': False,
            'enableRateLimit': True
        },
        'custom': {
            'url_templates': {
                'spot': "https://www.bitmart.com/trade/en?symbol={base_currency}_{quoted_currency}"
            }
        }
    }
}
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

merged_config = {
    name: {**config[name], **config_credentials.get(name, {})}
    for name in config
}

def main():
    parser = argparse.ArgumentParser(description="Arbitrage CLI")
    parser.add_argument("--show-config", action="store_true", help="Показать merged_config")
    parser.add_argument("--exchange", type=str, help="Биржа для вывода информации")
    args = parser.parse_args()

    if args.show_config:
        import pprint
        pprint.pprint(merged_config)
        return

    if args.exchange:
        exch = args.exchange.lower()
        if exch in merged_config:
            print(f"Config for {exch}:")
            import pprint
            pprint.pprint(merged_config[exch])
        else:
            print(f"Exchange '{exch}' not found in config.")
        return

    parser.print_help()

if __name__ == "__main__":
    main()
