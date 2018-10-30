import tornado


class LoginHandler(tornado.web.RequestHandler):
    def initialize(self, baseurl, check_pin_usecase):
        self.baseurl = baseurl
        self.check_pin_usecase = check_pin_usecase

    def get(self):
        self.render("login.html", title="Pi Doorman")

    def post(self):
        if self.check_pin_usecase.execute(self.get_argument("pin")):
            self.set_secure_cookie("pin", self.get_argument("pin"))
            self.redirect("{}/".format(self.baseurl))
        else:
            self.set_secure_cookie("pin", None)
            self.redirect("{}/login".format(self.baseurl))
