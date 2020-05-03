import configparser
import logging
from argparse import ArgumentParser

import firebase_admin
import os
import tornado.ioloop
import tornado.web
from firebase_admin import credentials

from core.check_pin_usecase import CheckPinUsecase
from core.open_usecase import OpenUsecase
from core.ring_bell_usecase import RingBellUsecase
from gateway.door_gateway import DoorGateway
from gateway.notification_gateway import NotificationGateway
from login.login_handler import LoginHandler
from logout.logout_handler import LogoutHandler
from main.main_handler import MainHandler
from open.open_handler import OpenHandler

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)


def get_arguments():
    parser = ArgumentParser()
    parser.add_argument("-c", "--config",
                        dest="config",
                        default="/etc/pi-doorman.conf")
    return parser.parse_args()


def get_config(args):
    config = configparser.ConfigParser(
        inline_comment_prefixes=('#', ';'),
        allow_no_value=True
    )
    config.read(args.config)

    return config


def read_config(config):
    return (config['doorman']['baseurl'],
            config['doorman']['secret'],
            str.strip(config['doorman']['pins']).split("\n"),
            int(config['doorman']['latch_pin']),
            int(config['doorman']['latch_release_duration']),
            int(config['doorman']['bell_pin']),
            int(config['doorman']['door_button_pin']),
            config['doorman']['service_account_keys_path'],
            config['doorman']['token'],
            config['doorman']['port'])


def make_app(baseurl,
             secret,
             pins,
             latch_pin,
             latch_release_duration,
             bell_pin,
             door_button_pin,
             service_account_keys_path,
             token,
             port):
    log.info("make_app")

    door_gateway = DoorGateway(latch_pin, latch_release_duration, bell_pin, door_button_pin)

    cred = credentials.Certificate(service_account_keys_path)
    firebase_app = firebase_admin.initialize_app(cred)

    notification_gateway = NotificationGateway(firebase_app)

    ring_bell_usecase = RingBellUsecase(door_gateway, notification_gateway, token)

    door_gateway.when_door_button_pressed = ring_bell_usecase.execute

    check_pin_usecase = CheckPinUsecase(pins)
    open_usecase = OpenUsecase(pins, door_gateway)

    app = tornado.web.Application(
        [(r"/", MainHandler, dict(baseurl=baseurl, check_pin_usecase=check_pin_usecase)),
         (r"/login", LoginHandler, dict(baseurl=baseurl, check_pin_usecase=check_pin_usecase)),
         (r"/open", OpenHandler, dict(baseurl=baseurl, open_usecase=open_usecase, check_pin_usecase=check_pin_usecase)),
         (r"/logout", LogoutHandler, dict(baseurl=baseurl)), ], cookie_secret=secret)

    app.listen(port)

    log.info('make_app:listening in %s', port)

    return app


if __name__ == "__main__":
    args = get_arguments()
    config = get_config(args)
    config_tuple = read_config(config)

    app = make_app(*config_tuple)

    tornado.ioloop.IOLoop.current().start()
