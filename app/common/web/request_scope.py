from app.globals import g


def get_request_id():
    return getattr(g, 'request_id', '')


def set_request_id(request_id: str):
    g.request_id = request_id


def set_user_info(user_info):
    g.user_info = user_info
