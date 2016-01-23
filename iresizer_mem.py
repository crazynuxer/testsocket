#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.httpserver
#import gc
import requests,os,sys,string,cStringIO,random
from PIL import Image

from raven.contrib.tornado import AsyncSentryClient
from raven.contrib.tornado import SentryMixin

''' generate random char '''
def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

''' Fungsi untuk download images dan menyimpan file'''
def resizeImage(url,filename,w=200,q=60):
    if not os.path.exists('/tmp/resize'):
       try:
           os.mkdir('/tmp/resize')
       except:
           sys.exit(0)
    try:
        getimg = requests.get(url)
        file_img = Image.open(cStringIO.StringIO(getimg.content))
        dictext = {'JPEG':'.jpg','PNG':'.png','GIF':'.gif','WEBP':'.jpg','PSD':'.jpg','BMP':'.jpg'}
        fileresize = '/tmp/resize/' + filename + dictext[file_img.format]
        formatfile = file_img.format
        if getimg.status_code != 200 or getimg.content == '':
            return None
        if w.isdigit():
            w = int(w)
            if w < 150:
               w = 150
        else:
            w = 200
        if q.isdigit():
            q = int(q)
        else:
            q = 60
        h = int(round((file_img.size[1] * w) / file_img.size[0]))
        size = (w,h)
        newfile = file_img.resize(size, Image.ANTIALIAS)
        newfile.save(fileresize,quality=int(q))
        del getimg,file_img,w,q,h,size,newfile,dictext
        return (fileresize,formatfile)
    except:
        return None


listhost = ['images.example.com']

class api(SentryMixin, tornado.web.RequestHandler):
    def initialize(self, *args, **kwargs):
        self.remote_ip = self.request.headers.get('X-Forwarded-For', self.request.headers.get('X-Real-Ip', self.request.remote_ip))
        self.host = self.request.headers.get('Host', self.request.headers.get('Host', self.request.host))
        self.using_ssl = (self.request.headers.get('X-Scheme', 'http') == 'https')
    def options(self):
        self.finish()
    def head(self):
        self.finish()
    def post(self):
        self.finish()
    def put(self):
        self.finish()
    def delete(self):
        self.finish()
    def get(self):
        filename = self.request.path.split('/')[-1]
        if self.host not in listhost:
            self.host = 'images.example.com'
            url = 'http://' + self.host + self.request.path + '?a=1'
        elif self.host == 'images.example2.com':
            self.host = 'images.example.com'
            path = self.request.path
            if path.startswith('/visual'):
                url = 'http://' + self.host + '/media' + self.request.path 
            else:
                url = 'http://' + self.host + '/media2' + self.request.path 
        else:
            url = 'http://' + self.host + self.request.path 
        print url
        if filename.endswith('.ico'):
            self.finish()
            return
        else:
            filename = filename + id_generator()
            dictquery = {}
            dictquery["q"] = self.get_argument("q", "80")
            dictquery["w"] = self.get_argument("w", "200")
            imagefile = resizeImage(url,filename,dictquery["w"],dictquery["q"])
            if imagefile is None:
                self.finish()
                return

            dictcontent = {'JPEG':'image/jpeg','PNG':'image/png','GIF':'image/gif','WEBP':'image/webp','BMP':'image/x-ms-bmp','PSD':'image/jpeg'}
            with open(imagefile[0], 'r') as f:
                self.set_header("Content-Type", dictcontent[imagefile[1]] + '; charset="utf-8"')
                data = f.read()
                self.write(data)
                self.finish()
            try:
                #hapus images
                os.unlink(imagefile[0])
                #print gc.collect(), "unreachable objects"
                del imagefile,filename,dictcontent,dictquery,url,path
            except:
                pass



if __name__ == "__main__":
    application = tornado.web.Application([
        (r".*", api),
    ])
    application.sentry_client = AsyncSentryClient('http://028fb2a4f8b14f17876897e78397e274:e4db2f71807148deb27d29ec3f78afff@sentry.example.com/30')

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.bind(80)
    http_server.start(0)
    tornado.ioloop.IOLoop.instance().start()

