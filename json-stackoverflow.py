#!/usr/bin/env python
## json-stackoverflow.py -- JSON Cricket -*- Python -*-
## Time-stamp: "2009-02-24 14:50:20 ghoseb"

## Copyright (c) 2009, oCricket.com

import os
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api.urlfetch import fetch, GET, DownloadError

from src.so_rep import get_so_info

class IndexPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
        self.response.out.write(template.render(path, template_values))

class ShowReputation(webapp.RequestHandler):
    def get(self):
        data = None
        sid = self.request.get("id")
        callback = self.request.get("callback")

        so_info = get_so_info(sid)

        if not so_info:
            self.response.out.write(data)
            return              # Exit the handler

        if callback:
            data = "%s(%s)" % (callback, so_info)
        else:
            data = so_info

        self.response.out.write(data)


class Widget(webapp.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "application/javascript"
        sid = self.request.get("id")
        path = os.path.join(os.path.dirname(__file__), 'templates', 'widget.js.txt')
        if not sid:
            self.error(400)
            return
        js = memcache.get(sid + ".js")
        if not js:
            js = template.render(path, {'id': sid})
            memcache.set(sid + ".js", js, 10 * 24 * 60 * 60) # 10 days

        return self.response.out.write(js)
        
        
application = webapp.WSGIApplication([('/', IndexPage),
                                      ('/reputation.json', ShowReputation),
                                      ('/widget.js', Widget),], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
