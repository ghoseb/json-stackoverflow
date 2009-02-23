#!/usr/bin/env python
## json-stackoverflow.py -- JSON Cricket -*- Python -*-
## Time-stamp: "2009-02-23 19:52:17 ghoseb"

## Copyright (c) 2009, oCricket.com

import os
import wsgiref.handlers
from google.appengine.ext import webapp
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


application = webapp.WSGIApplication([('/', IndexPage),
                                      ('/reputation.json', ShowReputation)], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
