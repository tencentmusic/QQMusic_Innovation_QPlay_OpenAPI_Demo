#! /usr/bin/env python3.7
# -*- coding: utf-8 -*-

import hashlib
import time
import urllib.parse
import configparser

config = configparser.ConfigParser()
config.read('OpenAPI.ini')

OPI_APP_ID = config['DEFAULT']['OPI_APP_ID']
OPI_APP_KEY = config['DEFAULT']['OPI_APP_KEY']
OPI_APP_PRIVATE_KEY = config['DEFAULT']['OPI_APP_PRIVATE_KEY']
OPI_DEVICE_ID = config['DEFAULT']['OPI_DEVICE_ID']
OPI_DEVICE_KEY = config['DEFAULT']['OPI_DEVICE_KEY']

# Define the URL components
URL_SCHEME = 'http'
# URL_SCHEME = 'https'
URL_NETLOC = 'openrpc.music.qq.com'
# URL_NETLOC = 'opensz.music.qq.com'
# URL_NETLOC = 'opensh.music.qq.com'
URL_PATH = '/rpc_proxy/fcgi-bin/music_open_api.fcg'
URL_PARAMETER = ''
URL_FRAGMENT = ''


def timestamp():
    return str(int(time.time()))


def common_query_signature(app_id, app_key, pri_key, ts):
    r"""Generate the signature used in query

    :param app_id: app_id, issued by OpenAPI
    :param app_key: app_key, issued by OpenAPI
    :param pri_key:
    :param ts: timestamp
    :return: a signature used as sign
    """
    plain_text = "OpitrtqeGzopIlwxs_%s_%s_%s_%s" % (app_id, app_key, pri_key, ts)
    m = hashlib.md5()
    m.update(plain_text.encode('utf-8'))
    return m.hexdigest()


def common_query_signature(app_id, app_key, pri_key, ts):
    r"""Generate the signature used in query

    :param app_id: app_id, issued by OpenAPI
    :param app_key: app_key, issued by OpenAPI
    :param pri_key:
    :param ts: timestamp
    :return: a signature used as sign
    """
    plain_text = "OpitrtqeGzopIlwxs_%s_%s_%s_%s" % (app_id, app_key, pri_key, ts)
    m = hashlib.md5()
    m.update(plain_text.encode('utf-8'))
    return m.hexdigest()


def common_query_str(ts):
    r"""Create the uncompleted dictionary of the query string,
    which contain aap_id, app_key, timestamp, sign, client_ip

    :param ts: timestamp
    :return: a uncompleted dictionary of the query string
    """

    signature_str = common_query_signature(OPI_APP_ID, OPI_APP_KEY, OPI_APP_PRIVATE_KEY, ts)
    args = {
        'app_id': OPI_APP_ID,
        'app_key': OPI_APP_KEY,
        'timestamp': ts,
        'sign': signature_str,
        'client_ip': '10.68.108.41',
    }
    return args


def request(cmd, args, openid_auth):
    r"""Generate URL with cmd, args

    :param cmd: command
    :param args: arguments of command
    :param openid_auth: arguments of qqmusic openid login
    :return: URL
    """

    ts = timestamp()
    common_query_args = common_query_str(ts)
    query_args = {**common_query_args, **openid_auth, **args}
    query_args['opi_cmd'] = cmd
    query_args['login_type'] = '5'
    query_args['user_login_type'] = '6'
    query_args['device_login_type'] = '4'
    query_args['opi_device_id'] = OPI_DEVICE_ID
    query_args['opi_device_key'] = OPI_DEVICE_KEY
    query = urllib.parse.urlencode(query_args)

    parse_result = urllib.parse.ParseResult(scheme=URL_SCHEME, netloc=URL_NETLOC, path=URL_PATH, query=query, params=URL_PARAMETER, fragment=URL_FRAGMENT)
    url = urllib.parse.urlunparse(parse_result)
    return url