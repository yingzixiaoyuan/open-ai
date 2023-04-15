# -*- coding: utf-8 -*-
'''
@project : sa
@author  : chulihui
@file   : portal.py
@time   : 2019-10-04 10:25
'''
import datetime
import logging

from app import config
from app.common.web.request_scope import set_user_info
from app.exceptions import InvalidBAError
from jose import jwt

logger = logging.getLogger(__name__)


class Portal(object):
    def __init__(self, request, client_secret):
        super().__init__()
        self._request = request
        self._client_secret = client_secret

    def validate(self):
        portal_sign = self.__get_portal_sign()
        if portal_sign:
            return self.decode_auth_token(portal_sign)
        else:
            raise InvalidBAError

    def __get_portal_sign(self):
        return self._request.headers.get('Authorization', '')

    @staticmethod
    def encode_auth_token(name):
        """
        生成认证Token
        :param name: str
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',
                'data': {
                    'name': name,
                }
            }

            return jwt.encode(
                payload,
                config.SECRET_KEY,
                algorithm=config.ALGORITHM
            )
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, config.SECRET_KEY, leeway=datetime.timedelta(seconds=10))
            if 'data' in payload and 'name' in payload['data']:
                return payload
        except Exception as e:
            logger.error(str(e), exc_info=True)
            raise InvalidBAError


def _get_fake_info(request):
    pass


def _skip(path, skip_urls):
    if path in skip_urls:
        return True
    else:
        return False


def portal_auth(request,skip_urls, use_fake_info):
    def _delegate():
        if _skip(request.url.path, skip_urls):
            return
        p = Portal(
            request=request,
            client_secret=config.SECRET_KEY
        )
        try:
            user_info = p.validate()
            set_user_info(user_info)
        except InvalidBAError as e:
            if use_fake_info:
                set_user_info(_get_fake_info(request))
                return
            logger.error(str(e), exc_info=True)
            raise InvalidBAError

    return _delegate
