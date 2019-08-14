#! /usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
Demonstrate how to utilize the interface: fcg_music_custom_vip_online_deliver.fcg
"""

import hashlib
import configparser
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


config = configparser.ConfigParser()
config.read('OpenAPI.ini')

DEV_AUTH_DEVICE_KEY = config['DEFAULT']['DEV_AUTH_DEVICE_KEY']
DEV_AUTH_SEED_PREFIX = config['DEFAULT']['DEV_AUTH_SEED_PREFIX']


def vip_online_deliver(timestamp):
    """
    Return the arguments of request, containing cmd, mch_id, tran_info
    :param timestamp: equals with the one in common arguments
    :return: a map with three arguments
    """

    # WARN: the below values must be modified on your need
    music_id = '15231959988270997673'
    tran_seq = '4'
    tran_date = '20190627'
    order_time = '1561638344'
    sell_type = '2'
    sell_sub_type = '2'
    num = '51'

    # Follow the rule: music_id__tran_seq__tran_date__order_time__sell_type__sell_sub_type__num
    plain_tran_info = "%s__%s__%s__%s__%s__%s__%s" % (music_id, tran_seq, tran_date, order_time, sell_type, sell_sub_type, num)

    m = hashlib.md5()
    m.update(DEV_AUTH_DEVICE_KEY.encode('utf-8'))
    aes_key = m.hexdigest()
    m = hashlib.md5()
    m.update(("%s_%s" % (DEV_AUTH_SEED_PREFIX, timestamp)).encode('utf-8'))
    aes_iv = m.hexdigest()
    cipher = AES.new(bytes.fromhex(aes_key), AES.MODE_CBC, bytes.fromhex(aes_iv))
    tran_info = cipher.encrypt(pad(plain_tran_info.encode('utf-8'), 16)).hex()

    cmd = 1     # 1：绿钻、付费包发货；2：绿钻、付费包状态查询
    mch_id = '123abc'
    query_args = {'cmd': cmd, 'mch_id': mch_id, 'tran_info': tran_info}
    return query_args
