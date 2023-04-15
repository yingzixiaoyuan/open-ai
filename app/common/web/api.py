import collections
import datetime
import decimal
import functools
import json

from app.common.web import exception, request_scope
from app.globals import g
from fastapi.responses import JSONResponse, Response


class DatetimeEncoder(json.JSONEncoder):
    """Provide encoder for datetime object"""

    def default(self, obj):
        if isinstance(obj, datetime.datetime) or isinstance(
                obj, datetime.date):
            # TODO(madongliang): 这里时间格式需要修改, 这边的规范不是标准格式
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        else:
            return json.JSONEncoder.default(self, obj)


def error_response(error: Exception):
    if isinstance(error, exception.WebError):
        code = error.code
        status_code = error.status_code
        message = error.message
        user_message = error.user_message
    else:
        code = -100
        status_code = 500
        message = repr(error)
        user_message = '未知错误'

    response = {
        'code': code,
        'message': message,
        'userMessage': user_message,
        'data': {},
        'ctx': {
            'requestId': request_scope.get_request_id(),
        }
    }
    return _nice_json(response, status_code=status_code)


def _nice_json(data, status_code):

    content = json.dumps(
        data,
        ensure_ascii=False,
        allow_nan=False,
        indent=None,
        separators=(",", ":"),
    ).encode("utf-8")
    response = Response(content=content, status_code=status_code)
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response


def _success(data=None, compress: bool = False):
    """API成功返回

    :param data: 要返回的json
    :param compress: 对于特别大的json, 为了优化性能, 可以对其进行压缩
    :type compress: bool
    """
    if data is None:
        data = {}
    if data.get("count"):
        response = {
            'code': 0,
            'userMessage': '操作成功',
            'message': '操作成功',
            'count': data.get('count'),
            'data': data.get('data'),
            'ctx': {
                'requestId': request_scope.get_request_id(),
            }
        }
    else:
        response = {
            'code': 0,
            'userMessage': '操作成功',
            'message': '操作成功',
            'data': data,
            'ctx': {
                'requestId': request_scope.get_request_id(),
            }
        }

    return _nice_json(
        data=response,
        status_code=200
    )


def json_response(compress=False):
    """将 Controller 返回的内置类型序列化成 json

    Usage: ::

        class Foo(flask_restful.Resource):
            @json_response
            def get(self):
                # 直接返回可以被序列化的内置对象即可
                return {
                    'foo': 'bar',
                    1: 233
                }

        class Foo(flask_restful.Resource):
            @json_response(compress=True)
            def get(self):
                # 直接返回可以被序列化的内置对象即可
                return {
                    'foo': 'bar',
                    1: 233
                }

    :param compress: fn | 是否压缩JSON
    """
    if isinstance(compress, collections.abc.Callable):
        return _JsonResponse()(compress)

    return _JsonResponse(compress=compress)


class _JsonResponse(object):
    """将 Controller 返回的内置类型序列化成 json"""

    def __init__(self, compress: bool = False):
        super().__init__()

        self._compress = compress

    def __call__(self, fn):
        @functools.wraps(fn)
        def _delegate(*args, **kwargs):
            data = fn(*args, **kwargs)

            return _success(
                data=data,
                compress=self._compress
            )

        return _delegate
