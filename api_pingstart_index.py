# -*- coding:utf-8 -*-

import json
import settings
import pymongo
import tornado.autoreload
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from handlers import AppListHandler,UploadHandler,DownloadHandler, LostHandler
define("port", default=9998, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/v1/upload', UploadHandler),
            (r'/v1/app_list', AppListHandler),
            (r'/v1/download', DownloadHandler),
            (r'/v1/lost', LostHandler)
        ]
        super(Application, self).__init__(handlers)
        conn = pymongo.Connection(
            settings.MONGODB_HOST,
            settings.MONGODB_PORT
        )
        db = conn[settings.MONGODB_DB]
        self.co = db[settings.MONGODB_COLLECTION]


if __name__ == "__main__":
    options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print "Application starts on port: ", options.port
    tornado.ioloop.IOLoop.instance().start()
