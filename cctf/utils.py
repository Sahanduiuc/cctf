# -*- coding: utf-8 -*-
"""
 CCTF
 - Author:      Daniel J. Umpierrez
 - Created:     08-10-20018
 - License:     UNLICENSE
"""
import collections as col
import http.client as http
import json
import sys
import time
import typing as tp
import urllib.request as rq
from urllib.parse import urlencode

_PRICE_URL = 'https://min-api.cryptocompare.com/data/price?{}'

_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0'

_HEADERS = {
    'User-Agent': _USER_AGENT,
    'Accept-Encoding': 'UTF-8',
    'Accept': '*/*',
    'Connection': 'keep-alive'
}


def get_url(url, params=None, retries=1, wait_secs=15, verbose=True):
    """Read URL content and return it as str type.

    >>> url = 'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD'
    >>> response = get_url(url, params={'fsym': 'BTC', 'tsym': 'USD'})
    >>> isinstance(response, dict) and 'USD' in  response.keys()
    True

    :param str url: URL to retrieve as str.
    :param dict params: params used to build the GET request.L
    :param int retries: max retries, if retries value is negative there is no attempts limit (default -1)
    :param int wait_secs: sleep time in secs between retries.
    :param bool verbose: if True all catches errors will be reported to stderr.
    :return str: raw url content as str type. In case of error, an empty string will be returned.
    """

    while retries > 0:
        try:
            # handler = rq.urlopen()  # type: rq.OpenerDirector
            params = urlencode(params or dict())
            request = rq.Request(url, headers=_HEADERS)
            response = rq.urlopen(request)  # type: http.HTTPResponse
            response = response.read()  # type: bytes
            response = response.decode(encoding='utf8')
            try:
                response = json.loads(response)
            except (json.JSONDecodeError, ValueError) as err:
                pass
                # print('"cctf.utils::get_url": {}'.format(str(err)))
            return response
        except http.InvalidURL:
            print('{} is not a valid URL'.format(str(url)))
            return str()
        except http.HTTPException as err:
            if verbose:
                print(str(err), file=sys.stderr)
                print(' - Retrying', file=sys.stderr)
            retries -= 1
            time.sleep(wait_secs)
        except IOError as err:
            return str(err)

        except KeyboardInterrupt:
            return str()


def _params(params):
    """Params handler.

    :param params:
    :type params: dict
    :return:
    """
    params = dict(params or {})

    for param in ['tsyms', 'fsyms']:
        if param in params:
            param_value = params.get(param)
            if isinstance(param_value, str) and ',' not in param:
                params[param] = [param_value]
            if isinstance(param_value, col.Iterable):
                params[param] = ','.join([str(s).upper() for s in param_value])
    return params


def get_price(base, quote=None):
    """Get price for a symbol from CryptoCompare.com

    >>> price = get_price('TRX')
    >>> isinstance(price, float) and price > 0.0
    True

    :param base: base currency.
    :type base: str or Currency
    :param quote: quote currency (default BTC).
    :type quote: str or Currency
    :return: current price for supplied currency pair.
    :rtype: float
    """
    quote = str(quote or 'BTC').strip(' T')
    if quote not in ['BTC', 'EUR', 'USD']:
        quote = 'BTC'
    params = {'fsym': base.upper(), 'tsyms': quote.upper()}
    params = urlencode(params)
    url = _PRICE_URL.format(params)
    result = get_url(url)
    return result.get(quote.upper())


# def get_price(fsyms: tp.Union[tp.Sequence[tp.Text], tp.Text],
#               tsyms: tp.Union[tp.Sequence[tp.Text], tp.Text]) -> tp.Dict:
#     """ Price conversion (one to many) from "fsym" currency to "tsyms" currencies.
#
#     >>> data = get_price(fsyms='BTC', tsyms=['ETH', 'USD', 'EUR'])
#     >>> isinstance(data, dict)
#     True
#     >>> all(isinstance(v, float) for v in data.values())
#     True
#     >>> data = get_price(['BTC', 'ETH', 'XRP', 'ADA'], ['USD', 'EUR'])
#     >>> isinstance(data, dict)
#     True
#     >>> isinstance(data['total'], float)
#     True
#
#     """
#     if isinstance(fsyms, str):
#         fsyms = [fsyms]
#     if isinstance(tsyms, str):
#         tsyms = [tsyms]
#
#     if len(fsyms) == 1 and len(tsyms) >= 1:
#         fsym = str(fsyms[0])
#         del fsyms
#         return get_url(_PRICE_URL, locals())
#     elif len(fsyms) > 1 and len(tsyms) >= 1:
#         return get_url(_PRICE_MULTI_URL, locals())
#     else:
#         raise ValueError()


def flt(value, p=None, as_str=False):
    """Float builtin wrapper for precision param initialization.

    :param bool as_str: return as string
    :param value:
    :type value: Number or str
    :param int p:
    :return:
    :rtype: str or Number
    """

    value_str = str(value or '0.0').strip()

    if '.' in value_str:
        template = '{{:.{:d}f}}'.format(p or infer_precision(value))
        value = template.format(float(value_str)).rstrip('.0')
        backup = str(value)
        try:
            value = value if as_str else float(value)
        except ValueError:
            value = backup
        return value
    elif value_str.lstrip('-+').rstrip('.').isnumeric():
        return int(value)
    else:
        return value


def infer_precision(number):
    """

    :param float number:
    :return int:
    """
    number = number or 0.0
    try:
        number = float(number)
    except ValueError:
        return number
    if number is not None and isinstance(number, float):
        if number < 0.000001:
            return 10
        elif number < 0.0001:
            return 8
        elif number < 0.01:
            return 5
        elif number < 1.0:
            return 3
        elif number < 100:
            return 2
        elif number < 1000:
            return 1
        else:
            return 0


def num2str(n, precision=8):
    """Numeric type infer and parser.

    Accept any Iterable (dict, list, tuple, set, ...) or built-in data types int, float, str, ... and try to
    convert it a number data type (int, float)

    :param n:
    :type n: Number or tp.Iterable
    :param int precision:
    :return tp.Iterable:
    """
    if n is not None:
        if isinstance(n, str):
            backup = type(n)(n)
            try:
                n = flt(n, precision, as_str=True)
            except ValueError:
                n = backup
        elif isinstance(n, str):
            n = flt(n, precision, as_str=True)
        elif isinstance(n, tp.Dict):
            n = {k: num2str(v, precision) if isinstance(v, col.Iterable) else v for k, v in dict(n).items()}
        elif isinstance(n, col.Iterable):
            n = [num2str(n, precision) if isinstance(n, col.Iterable) else n for n in list(n)]
    return n


if __name__ == '__main__':
    _COIN_LIST_URL = 'https://min-api.cryptocompare.com/data/all/coinlist'
    resp = get_url(_COIN_LIST_URL)
    print(len(resp.get('Data', {}).keys()))
