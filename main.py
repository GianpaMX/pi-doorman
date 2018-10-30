import configparser
from argparse import ArgumentParser

import tornado.ioloop
import tornado.web

from core.check_pin_usecase import CheckPinUsecase
from core.open_usecase import OpenUsecase
from gateway.door_gateway import DoorGateway
from login.login_handler import LoginHandler
from logout.logout_handler import LogoutHandler
from main.main_handler import MainHandler
from open.open_handler import OpenHandler


def make_app(baseurl, secret, pins, gpiopin, duration):
    door_gateway = DoorGateway(gpiopin, duration)

    check_pin_usecase = CheckPinUsecase(pins)
    open_usecase = OpenUsecase(pins, door_gateway)

    return tornado.web.Application([
        (r"/", MainHandler, dict(
            baseurl=baseurl,
            check_pin_usecase=check_pin_usecase)),
        (r"/login", LoginHandler, dict(
            baseurl=baseurl,
            check_pin_usecase=check_pin_usecase)),
        (r"/open", OpenHandler, dict(
            baseurl=baseurl,
            open_usecase=open_usecase,
            check_pin_usecase=check_pin_usecase)),
        (r"/logout", LogoutHandler, dict(
            baseurl=baseurl)),
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
