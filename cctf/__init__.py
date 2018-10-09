# -*- coding: utf-8 -*-
"""
 CCTF: Crypto-Currencies Trading Framework.
"""
from cctf.balance import Balance, Wallet
from cctf.core import Range, Precision, Limits
from cctf.market import Markets, Market, Tickers, Ticker
from cctf.symbol import Symbol, Symbols, Currency, Currencies, CURRENCIES

__project__ = 'CCTF'
__package__ = 'cctf'
__description__ = __doc__
__author__ = 'Daniel J. Umpierrez'
__version__ = '0.1.1'
__license__ = 'MIT'
__site__ = 'https://github.com/havocesp/{}'.format(__package__)
__email__ = 'umpierrez@pm.me'
__dependencies__ = list()
__deplinks__ = ['https://github.com/havocesp/cryptocmp', 'https://github.com/havocesp/logging4humans']
__keywords__ = ['altcoins', 'altcoin', 'exchange', 'bitcoin', 'trading']

__all__ = ['__description__', '__author__', '__license__', '__version__', '__package__', '__project__', '__site__',
           '__email__', '__keywords__', 'Range', 'Precision', 'Limits', 'Symbol', 'Symbols', 'Currency', 'Currencies',
           'CURRENCIES', 'Markets', 'Market', 'Tickers', 'Ticker', 'Balance', 'Wallet', '__deplinks__',
           '__dependencies__']
