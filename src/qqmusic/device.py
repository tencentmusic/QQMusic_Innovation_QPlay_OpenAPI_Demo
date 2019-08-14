#! /usr/bin/env python3.7
# -*- coding: utf-8 -*-

import argparse
import hashlib
import urllib.parse
import configparser
from urllib.parse import ParseResult, urlunparse
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_der_private_key
from cryptography.hazmat.backends import default_backend
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES

from qqmusic import openapi

config = configparser.ConfigParser()
config.read('OpenAPI.ini')

DEV_AUTH_DEVICE_KEY = config['DEFAULT']['DEV_AUTH_DEVICE_KEY']
DEV_AUTH_SEED_PREFIX = config['DEFAULT']['DEV_AUTH_SEED_PREFIX']
DEV_AUTH_PRI_KEY = config['DEFAULT']['DEV_AUTH_PRI_KEY']
DEV_AUTH_PID = config['DEFAULT']['DEV_AUTH_PID']
DEV_AUTH_SN = config['DEFAULT']['DEV_AUTH_SN']

# Define the URL components
URL_SCHEME = 'http'
URL_NETLOC = 'open.music.qq.com'
URL_PATH = '/fcgi-bin/fcg_music_custom_third_party_account_auth.fcg'
URL_PARAMETER = ''
URL_FRAGMENT = ''


def issue_licence(sign_source, pri_key):
    r"""Generate a licence by RSA signing with Private Key.

    :param sign_source: the plain text to be signed
    :param pri_key: private key. See the document by QQMusic.
    :return: the bytes of licence (signature)
    """

    license_bytes = pri_key.sign(sign_source.encode('utf-8'), padding.PKCS1v15(), hashes.SHA1())
    return license_bytes


def load_private_hex_key(key_hex_str):
    r"""Load the private key, which is in HEX model, required by OpenAPI.
    Note: it's in der format.

    :param key_hex_str: a string of a private key, in HEX model.
    :return: private key object
    """

    return load_der_private_key(bytearray.fromhex(key_hex_str), password=None, backend=default_backend())


def encrypt_device_info(dev_key, seed_prefix, ts, dev_info):
    r"""Encrypt the device info

    :param dev_key: DeviceKey, issued by OpenAPI.
    :param seed_prefix: DeviceSeedPrefix, issued by OpenAPI
    :param ts: timestamp
    :param dev_info: device info
    :return: encrypted text
    """

    m = hashlib.md5()
    m.update(dev_key.encode('utf-8'))
    aes_key = m.hexdigest()
    m = hashlib.md5()
    m.update(("%s_%s" % (seed_prefix, ts)).encode('utf-8'))
    aes_iv = m.hexdigest()
    cipher = AES.new(bytes.fromhex(aes_key), AES.MODE_CBC, bytes.fromhex(aes_iv))
    ct = cipher.encrypt(pad(dev_info.encode('utf-8'), 16))
    return ct


def device_login_query_str(ts, cmd):
    r"""Create the dictionary of the query string,
    which contain third_part_account and crypto_seed

    :param ts: timestamp
    :param cmd: cmd, register or login
    :return: a dictionary of the query string
    """

    pri_key = load_private_hex_key(DEV_AUTH_PRI_KEY)
    sign_source = "%s__,,__%s__,,__%s" % (DEV_AUTH_PID, DEV_AUTH_SN, ts)
    license_hex = (issue_licence(sign_source, pri_key)).hex()
    device_info = "%s__,,__%s" % (sign_source, license_hex)
    encrypted_device_info = encrypt_device_info(DEV_AUTH_DEVICE_KEY, DEV_AUTH_SEED_PREFIX, ts, device_info)
    device_args = {'third_part_account': encrypted_device_info.hex(), 'crypto_seed': ts}
    common_args = openapi.common_query_str(ts)
    query_args = {**common_args, **device_args}
    query_args['cmd'] = cmd
    return query_args


def device_auth(cmd):
    ts = openapi.timestamp()
    query_args = device_login_query_str(ts, cmd)
    query = urllib.parse.urlencode(query_args)
    parse_result = ParseResult(scheme=URL_SCHEME, netloc=URL_NETLOC, path=URL_PATH, query=query, params=URL_PARAMETER, fragment=URL_FRAGMENT)
    url = urlunparse(parse_result)
    return url


def main():
    parser = argparse.ArgumentParser(description='Generate Device Authentication Request URL')
    parser.add_argument('--cmd', metavar='command', default='login', choices=['login', 'register'],
                        help='command of Device Authentication (default: login)')
    args = parser.parse_args()
    print(device_auth(args.cmd))


if __name__ == '__main__':
    main()
