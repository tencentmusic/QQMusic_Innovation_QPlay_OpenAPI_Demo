#! /usr/bin/env python3.7
# -*- coding: utf-8 -*-

import configparser

config = configparser.ConfigParser()
config.read('OpenAPI.ini')

QQMUSIC_OPENID_APPID = config['DEFAULT']['QQMUSIC_OPENID_APPID']
QQMUSIC_OPENID_USERID = config['DEFAULT']['QQMUSIC_OPENID_USERID']
QQMUSIC_ACCESS_TOKEN = config['DEFAULT']['QQMUSIC_ACCESS_TOKEN']


def qqmusic_login_str(open_app_id, open_id, access_token):
    r"""User login with QQMusic OpenID

    :param open_app_id: qqmusic_open_appid
    :param open_id: qqmusic_open_id
    :param access_token: qqmusic_access_token
    :return: a dictionary with three arguments
    """

    query_args = {'qqmusic_open_appid': open_app_id, 'qqmusic_open_id': open_id, 'qqmusic_access_token': access_token}
    return query_args