import logging

import webapp2
from google.appengine.api import urlfetch
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

import issues


class LogSenderHandler(InboundMailHandler):

    def receive(self, mail_message):
        logging.info('Received message from: %s', mail_message.sender)
        logging.info('Subject: %s', mail_message.subject)
        issues.create_issue(mail_message, issues.get_config(), urlfetch.fetch, urlfetch.POST)
        return
        

app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)
