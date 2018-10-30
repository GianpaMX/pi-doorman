import tornado


class LogoutHandler(tornado.web.RequestHandler):
    def initialize(self, baseurl):
        self.baseurl = baseurl

    def get(self):
        self.clear_cookie("pin")
        self.redirect("{}/login".format(self.baseurl))
