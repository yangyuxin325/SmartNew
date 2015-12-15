#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年4月7日

@author: sanhe
'''

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

if __name__ == "main":
    application = tornado.web.Application([
                                           (r"/",MainHandler)
                                           ,])
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()