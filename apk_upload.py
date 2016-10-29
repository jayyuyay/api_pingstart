# coding=utf-8
import os
import tornado.gen
from tornado.web import asynchronous
import tornado.httpclient

@asynchronous
@tornado.gen.coroutine
def upload_apk(self):
    """
    """
    upload_path = os.path.join(os.path.dirname(__file__), 'upload/')
    resp = self.request.files['file'][0]
    body = resp['body']
    cname = resp['filename']
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    fpath = upload_path + cname
    with open(fpath, 'wb') as f:
        f.write(body)
    self.finish()


