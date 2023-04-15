# -*- encoding: utf-8 -*-

# @File    : main.py
# @Time    : 2021/11/06 21:39:28



import uvicorn

from app import get_app

app = get_app()


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
