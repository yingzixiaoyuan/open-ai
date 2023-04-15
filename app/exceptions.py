# -*- encoding: utf-8 -*-

# @File    : exception.py
# @Time    : 2021/11/09 09:31:49

from app.common.web.exception import (AccessError, BadRequestError,
                                      InternalServerError, InvalidParamError,
                                      NotFoundError, UnauthorizedError,
                                      ensure_code_not_duplicate)


class NotAuthenticatedException(Exception):
        pass

class AuthorizedError(UnauthorizedError):
    message = 'Account Password Error'
    user_message = '账号密码错误'

class RouteNotFound(NotFoundError):
    message = 'Route Not Found'
    user_message = '路由未找到'


class InvalidBAError(AccessError):
    message = 'Access denied: invalid BA'
    user_message = '无权限'


class ORMActionError(InternalServerError):
    message = 'Orm action error'
    user_message = 'orm 操作出错'


class ResourceExist(InternalServerError):
    message = 'Resource existed'
    user_message = '资源已经存在'
    code = 506


class ResourceNotFound(NotFoundError):
    message = 'Resource Not Found'
    user_message = '资源未找到'
    code = 406
ensure_code_not_duplicate(globals())
