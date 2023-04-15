import collections.abc

_IGNORE_NAMES = {
    'WebError',
    'InvalidParamError',
    'BadRequestError',
    'UnauthorizedError',
    'AccessError',
    'NotFoundError',
    'InternalServerError',
}


class WebError(Exception):
    message = "An unknown exception message"
    user_message = "内部错误"
    status_code = 500
    code = 500

    def __init__(self, message=None, user_message=None, code=None):
        if message is not None:
            self.message = message
        if user_message is not None:
            self.user_message = user_message
        if code is not None:
            self.code = code

        super(WebError, self).__init__(self.message)

    @classmethod
    def simple_error_builder(cls, key):
        return cls(
            message=f'{cls.message}: {key}',
            user_message=f'{cls.user_message}: {key}'
        )

    @classmethod
    def build_error_with_extra_message(cls, extra_message):
        return cls(
            message=f'{cls.message}: {extra_message}'
        )

    def __repr__(self) -> str:
        return "{class_name}{ctx!r}".format(
            class_name=self.__class__.__name__,
            ctx={
                "message": self.message,
                "user_message": self.user_message,
                "status_code": self.status_code,
                "code": self.code
            }
        )
    __str__ = __repr__


def ensure_code_not_duplicate(g: collections.abc.Mapping):
    """确保项目中定义的异常类 code 不重复

    Usage: ::

        ensure_code_not_duplicate(globals())

    :param g: globals()
    """
    error_codes = {}

    for name in g.keys():
        cls = g[name]

        if _need_ignore(name, cls):
            continue

        if cls.code not in error_codes:
            error_codes[cls.code] = name
            continue

        msg = '错误码重复: {new} {old}'.format(
            new=name,
            old=error_codes[cls.code]
        )

        raise Exception(msg)


class InvalidParamError(WebError):
    message = 'Invalid param'
    user_message = '参数错误'
    status_code = 400
    code = 400


class BadRequestError(WebError):
    message = 'Bad Request'
    user_message = '请求错误'
    status_code = 400
    code = 400


class UnauthorizedError(WebError):
    message = 'Unauthorized'
    user_message = '未认证'
    status_code = 401
    code = 401


class AccessError(WebError):
    message = 'Access denied'
    user_message = '无权限'
    status_code = 403
    code = 403


class NotFoundError(WebError):
    message = 'Not Found'
    user_message = '未找到'
    status_code = 404
    code = 404


class InternalServerError(WebError):
    message = 'Internal Server Error'
    user_message = '内部错误'
    status_code = 500
    code = 500


def _need_ignore(name: str, cls) -> bool:
    if name in _IGNORE_NAMES:
        return True

    if not isinstance(cls, type):
        return True

    if not issubclass(cls, WebError):
        return True

    return False
