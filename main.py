import configparser
from argparse import ArgumentParser

import tornado.ioloop
import tornado.web

from core.check_pin_usecase import CheckPinUsecase
from login.login_handler import LoginHandler


class MainHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("pin")

    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return

        self.write("Hello, world")


def make_app(secret, pins):
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler, dict(check_pin_usecase=CheckPinUsecase(pins))),
    ], cookie_secret=secret)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-c", "--config",
                        dest="config",
                        default="/etc/doorman.conf")

    args = parser.parse_args()

    config = configparser.ConfigParser(
        inline_comment_prefixes=('#', ';'),
        allow_no_value=True
    )
    config.read(args.config)

    secret = config['doorman']['secret']
    pins = str.strip(config['doorman']['pins']).split("\n")
    app = make_app(secret, pins)
    app.listen(config['doorman']['port'])
    tornado.ioloop.IOLoop.current().start()
