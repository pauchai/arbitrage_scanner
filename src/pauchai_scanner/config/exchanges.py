import os

from dotenv import load_dotenv
load_dotenv()
config = {
    'binance': {
        'enabled': True,
            'ccxt': {
                'options': {'defaultType': 'spot'},
            },
        'custom': {
            'logo_url': "https://github.com/user-attachments/assets/e9419b93-ccb0-46aa-9bff-c883f096274b",
            'urls': {
                'referral': "https://www.binance.com/activity/referral-entry/CPA?ref=CPA_00JM9DOEP3",
            },
            'url_templates': {
                'spot': "https://www.binance.com/en/trade/{base_currency}_{quoted_currency}?type=spot"
            }
        }
    },
    'bybit': {
        'enabled': True,
            'ccxt': {
                'options': {'defaultType': 'spot'},
            },
        'custom': {
            "logo_url": "https://github.com/user-attachments/assets/97a5d0b3-de10-423d-90e1-6620960025ed",
            "urls": {
                'referral': "https://www.bybit.com/invite?ref=ZL4WLP8"
            },
            'url_templates': {
                'spot': "https://www.bybit.com/trade/spot/{base_currency}/{quoted_currency}"
            }
        }
    },
    'bingx': {
        'enabled': True,
            'ccxt': {
                'options': {'defaultType': 'spot'},
            },
        'custom': {
            'logo_url': "https://github-production-user-asset-6210df.s3.amazonaws.com/1294454/253675376-6983b72e-4999-4549-b177-33b374c195e3.jpg",
            'urls': {
                'referral': "https://bingx.com/invite/GJKWDY/"
            },
            'url_templates': {
                'spot': "https://bingx.com/en/spot/{base_currency}{quoted_currency}/"
            }
        }
    },
    'kucoin': {
        'enabled': True,
            'ccxt': {
                'options': {'defaultType': 'spot'},
            },
        'custom': {
            'logo_url': "https://user-images.githubusercontent.com/51840849/87295558-132aaf80-c50e-11ea-9801-a2fb0c57c799.jpg",
            'urls': {
                'referral': "https://www.kucoin.com/r/rf/CX8XUX73"
            },
            'url_templates': {
                'spot': "https://www.kucoin.com/trade/{base_currency}-{quoted_currency}"
            }
        }
    },
    'okx': {
        'enabled': False ,  # временно отключена из-за проблем с API
            'ccxt': {
                'options': {'defaultType': 'spot'},
            },
        'custom': {
            'logo_url': "https://user-images.githubusercontent.com/1294454/152485636-38b19e4a-bece-4dec-979a-5982859ffc04.jpg",
            'urls': {
                #'referral': "https://www.okx.com/join/"  TODO: добавить реферальный код
            },
            'url_templates': {  
                'spot': "https://www.okx.com/trade/{base_currency}-{quoted_currency}"
            }
        }
    },
    'mexc': {
        'enabled': True,# временно отключена нет API ключей
            'ccxt': {
                'options': {'defaultType': 'spot'},
            },
        'custom': {
            'logo_url': "https://user-images.githubusercontent.com/1294454/137283979-8b2a818d-8633-461b-bfca-de89e8c446b2.jpg",
            'urls': {
                'referral': "https://promote.mexc.com/r/QpfKQfw8"
            },
            'url_templates': {
                'spot': "https://www.mexc.com/exchange/{base_currency}_{quoted_currency}"
            }
        }
    },
    'htx': {
        'enabled': True,# временно отключена нет API ключей
            'ccxt': {
                'options': {'defaultType': 'spot'},
            },
        'custom': {
            'logo_url': "https://user-images.githubusercontent.com/1294454/76137448-22748a80-604e-11ea-8069-6e389271911d.jpg",
            'urls': {
                'referral': "https://www.htx.com/invite/ru-ru/1f?invite_code=4g7jd223"
            },
            'url_templates': {
                'spot': "https://www.hathor.exchange/trade/{base_currency}-{quoted_currency}"
            }
        }
    },
    "bitmart": {
        'enabled': True,# временно отключена нет API ключей
            'ccxt': {
            'options': {'defaultType': 'spot'},
            },
        'custom': {
            'logo_url': "https://github.com/user-attachments/assets/0623e9c4-f50e-48c9-82bd-65c3908c3a14",
            'urls': {
                'referral': "https://www.bitmart.com/invite/cVxrKu"
            },
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
