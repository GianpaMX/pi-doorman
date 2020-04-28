import logging

import tornado

log = logging.getLogger(__name__)


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, baseurl, check_pin_usecase):
        self.baseurl = baseurl
        self.check_pin_usecase = check_pin_usecase

    def get_current_user(self):
        return self.get_secure_cookie("pin")

    def get(self):
        if not self.current_user:
            log.info('get:not_logged_in')
            self.redirect("{}/login".format(self.baseurl))
            return

        if not self.check_pin_usecase.execute(self.current_user.decode()):
            log.info('get:invalid_ping:%s', self.current_user.decode())
            self.clear_cookie("pin")
            self.redirect("{}/login".format(self.baseurl))
            return

        self.redirect("{}/open".format(self.baseurl))
