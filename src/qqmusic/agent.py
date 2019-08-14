#! /usr/bin/env python3.7
# -*- coding: utf-8 -*-

import argparse

from qqmusic import auth, openapi


def main():
    parser = argparse.ArgumentParser(description='Generate the request string')
    parser.add_argument('cmd', metavar='cmd', help='Command of OpenAPI')
    parser.add_argument('--cmd_args', nargs='*', help='Argument(s) of the cmd, like "key=value"')

    user_login_qqmusic = parser.add_argument_group('User Login - QQMusic OpenID')
    user_login_qqmusic.add_argument('--qm_app_id', help='APP id of OpenID', default=auth.QQMUSIC_OPENID_APPID)
    user_login_qqmusic.add_argument('--qm_user_id', help='User id of OpenID', default=auth.QQMUSIC_OPENID_USERID)
    user_login_qqmusic.add_argument('--qm_token', help='Token of OpenID', default=auth.QQMUSIC_ACCESS_TOKEN)

    device_login = parser.add_argument_group('Device Login')
    device_login.add_argument('--opi_dev_id', help='OpenAPI Device ID', default=openapi.OPI_DEVICE_ID)
    device_login.add_argument('--opi_dev_key', help='OpenAPI Device Key', default=openapi.OPI_DEVICE_KEY)

    args = parser.parse_args()

    cmdargs = {}
    if args.cmd_args:
        for arg in args.cmd_args:
            kv = arg.split("=")
            cmdargs[kv[0]] = kv[1]

    openid_auth = auth.qqmusic_login_str(args.qm_app_id, args.qm_user_id, args.qm_token)
    url = openapi.request(args.cmd, cmdargs, openid_auth)
    print(url)


if __name__ == '__main__':
    main()



