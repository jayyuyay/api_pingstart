# -*- coding:utf-8 -*-
from offer_list import app_list
import tornado.web
import yajl
import tornado.gen
from tornado.web import asynchronous
from gp_app import get_from_gp
from apk_upload import upload_apk
import os
import commands

manual = True


class AppListHandler(tornado.web.RequestHandler):
    """
    api_format: 45.33.61.253:9998/v1/app_list
    """
    @property
    def co(self):
        return self.application.co

    def get(self):
        if manual:
            # apps = []
            # for app in app_list:
            #     if not self.co.find_one(dict(pkg=app['pkg'])):
            #         self.co.save(app)
            #         apps.append(app)
            # for app in apps:
            #     app.pop('_id')
            # self.write(yajl.dumps(apps))
            self.write(yajl.dumps(app_list))
        else:
            app_to_up = []
            apps = self.co.find()
            for app in apps:
                V = get_from_gp(app['pkg'])
                app_version = V['version']
                if app['version'] != app_version:
                    self.co.update({'pkg': app['pkg']}, {'pkg': app['pkg'], 'version': app_version})
                    app_to_up.append(V)
            self.write(yajl.dumps(app_to_up))


class DownloadHandler(tornado.web.RequestHandler):

    def download(self,fpath,pkg):
        with open(fpath, 'rb') as f:
            self.set_header('Content-Type', 'application/vnd.android.package-archive')
            self.set_header('Content-Disposition', 'attachment; filename={0}'.format(pkg))
            self.write(f.read())
            self.finish()

    @asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
        api: 45.33.61.253:9998/v1/download?pkg={}

        """
        download_path = os.path.join(os.path.dirname(__file__), 'upload/')
        pkg = self.get_argument('pkg')
        fpath = download_path + pkg
        tornado.gen.Task(self.download(fpath,pkg))


class UploadHandler(tornado.web.RequestHandler):
    @asynchronous
    @tornado.gen.coroutine
    def post(self):
        """

        api : 45.33.61.253:9998/v1/upload
        """
        tornado.gen.Task(upload_apk(self))


class LostHandler(tornado.web.RequestHandler):
    @asynchronous
    @tornado.gen.coroutine
    def get(self):
        (status, output) = commands.getstatusoutput('ls ./upload | grep -v "applist" > ./upload/applist')
        l = []
        with open('./upload/applist', 'r') as f:
            for line in f:
                l.append(line.strip()[0:-4].replace('_', '.'))
        v = []
        for pkg in app_list:
            if pkg['pkg'] not in l:
                v.append(pkg)
        self.write(yajl.dumps(v))
