import tornado


class LoginHandler(tornado.web.RequestHandler):
    def initialize(self, baseurl, check_pin_usecase):
        self.baseurl = baseurl
        self.check_pin_usecase = check_pin_usecase

    def get(self):
        if self.get_secure_cookie("pin") \
                and self.check_pin_usecase.execute(self.get_secure_cookie("pin").decode()):
            self.redirect("{}/".format(self.baseurl))
        else:
            self.render("login.html", title="Pi Doorman", baseurl=self.baseurl)

    def post(self):
        if self.check_pin_usecase.execute(self.get_argument("pin")):
            self.set_secure_cookie("pin", self.get_argument("pin"))
            self.redirect("{}/".format(self.baseurl))
        else:
            self.clear_cookie("pin")
            self.redirect("{}/login".format(self.baseurl))
