#!/usr/bin/env python
## not_found.py -- JSON Cricket -*- Python -*-
## Time-stamp: "2009-02-12 12:43:56 ghoseb"

## Copyright (c) 2009, oCricket.com

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class NotFound(webapp.RequestHandler):
    def get(self):
        """
        """
        self.error(404)

application = webapp.WSGIApplication([('/', NotFound)], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

