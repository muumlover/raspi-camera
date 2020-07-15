# !/usr/bin/env python
# encoding: utf-8

"""
@Time    : 2020/6/18 20:46
@Author  : Sam Wang
@Email   : muumlover@live.com
@Blog    : https://blog.ronpy.com
@Project : raspi-camera
@FileName: main.py
@Software: PyCharm
@license : (C) Copyright 2020 by Sam Wang. All rights reserved.
@Desc    :

"""
import gzip
import logging

from aiohttp import web

from camera_pi import Camera

logging.basicConfig(
    format='%(levelname)s: %(asctime)s [%(pathname)s:%(lineno)d] %(message)s',
    level=logging.NOTSET
)

camera = Camera()


async def handle_preview(request):
    global camera
    return web.Response(
        content_type='image/jpeg',
        body=gzip.compress(camera.get_frame()),
        headers={
            "Content-Encoding": "gzip"
        }
    )


async def handle(request):
    with open('index.html', 'rb') as fp:
        content = fp.read()
    return web.Response(body=content, content_type='text/html')


app = web.Application()
app.add_routes([
    web.get('/', handle),
    web.get('/preview', handle_preview),
])

if __name__ == '__main__':
    web.run_app(app)
