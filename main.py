import configparser
from argparse import ArgumentParser

import tornado.ioloop
import tornado.web

from core.check_pin_usecase import CheckPinUsecase
from core.open_usecase import OpenUsecase
from gateway.door_gateway import DoorGateway
from login.login_handler import LoginHandler
from logout.logout_handler import LogoutHandler
from open.open_handler import OpenHandler


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, baseurl):
        self.baseurl = baseurl

    def get_current_user(self):
        return self.get_secure_cookie("pin")

    def get(self):
        if not self.current_user:
            self.redirect("{}/login".format(self.baseurl))
            return

        self.redirect("{}/open".format(self.baseurl))


def make_app(baseurl, secret, pins, gpiopin, duration):
    return tornado.web.Application([
        (r"/", MainHandler, dict(baseurl=baseurl)),
        (r"/login", LoginHandler, dict(baseurl=baseurl, check_pin_usecase=CheckPinUsecase(pins))),
        (r"/open", OpenHandler, dict(baseurl=baseurl, open_usecase=OpenUsecase(DoorGateway(gpiopin, duration)))),
        (r"/logout", LogoutHandler, dict(baseurl=baseurl)),
    ], cookie_secret=secret)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-c", "--config",
                        dest="config",
                        default="/etc/pi-doorman.conf")

    args = parser.parse_args()

    config = configparser.ConfigParser(
        inline_comment_prefixes=('#', ';'),
        allow_no_value=True
    )
    config.read(args.config)

    baseurl = config['doorman']['baseurl']
    secret = config['doorman']['secret']
    gpiopin = int(config['doorman']['gpiopin'])
    duration = int(config['doorman']['duration'])
    pins = str.strip(config['doorman']['pins']).split("\n")

    app = make_app(baseurl, secret, pins, gpiopin, duration)
    app.listen(config['doorman']['port'])
    tornado.ioloop.IOLoop.current().start()
