#!/usr/bin/python

import tornado.httpserver
import tornado.options
import tornado.web
import tornado.ioloop
import os.path
import torndb
import tornado.gen
import time


from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="sunbox", help="blog database name")
define("mysql_user", default="root", help="blog database user")
define("mysql_password", default="fengmxx", help="blog database password")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/update", UpdateHandler),
            (r"/stat", StatHandler),
            ]
        settings = dict(
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                ui_modules={"Onentry": EntryModule},
                debug=True,
                )
        self.db = torndb.Connection(host=options.mysql_host, database=options.mysql_database,
                user=options.mysql_user, password=options.mysql_password)
        tornado.web.Application.__init__(self, handlers, **settings)


class HomeHandler(tornado.web.RequestHandler):
#    @tornado.web.asynchronous
#    @tornado.gen.engine
    def get(self):
        entries = self.application.db.query("select id, location, uptime, last from sunbox.0 where unix_timestamp(last) >= unix_timestamp() - 900000;")
#        self.finish()
        self.render("index2.html")
    def post(self):
        name = self.get_argument("location")
        entries = self.application.db.query("select id, location, uptime, last from sunbox.0 where location='%s'" % name)
        print entries
        self.render("search.html" ,entries = entries)
class UpdateHandler(tornado.web.RequestHandler):
    def get(self):
        pass


class StatHandler(tornado.web.RequestHandler):
    def get(self):
        pass

class EntryModule(tornado.web.UIModule):
    def render(self, entry):
        return self.render_string(
                "modules/entry.html",
                entry=entry,
                )

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__=="__main__":
    main()
