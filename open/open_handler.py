import tornado


class OpenHandler(tornado.web.RequestHandler):
    def initialize(self, open_usecase):
        self.open_usecase = open_usecase

    def get_current_user(self):
        return self.get_secure_cookie("pin")

    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return

        self.render("open.html", title="Pi Doorman")

    def post(self):
        if not self.current_user:
            self.redirect("/login")
            return

        self.open_usecase.execute()
        self.redirect("/open")
