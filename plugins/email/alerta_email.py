import json
import logging
import os
import requests
import traceback
import ast

from alerta.plugins import PluginBase


class AlertaEmailPlugin(PluginBase):

    def __init__(self, name=None):
        super(AlertaEmailPlugin, self).__init__(name)

    def pre_receive(self, alert):
        return alert

    def post_receive(self, alert, rule_id, **kwargs):
        plugin_properties = self.get_properties(rule_id, 'email')
        contacts = plugin_properties['emails']
        subject = self._subject_template.render(alert=alert)
        text = alert.text
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Header(subject, 'utf-8').encode()
        msg['From'] = OPTIONS['mail_from']
        msg['To'] = ", ".join(contacts)
        msg.preamble = msg['Subject']
        msg_text = MIMEText(text, 'plain', 'utf-8')
        msg.attach(msg_text)
        try:
            self._send_email_message(msg, contacts)
        except smtplib.SMTPException as e:
            logging.getLogger('').error('Failed to send mail to %s on %s:%s : %s',
                                        ", ".join(contacts),
                                        OPTIONS['smtp_host'], OPTIONS['smtp_port'], e)
        except (socket.error, socket.herror, socket.gaierror) as e:
            logging.getLogger('').error('Mail server connection error: %s', e)
        except Exception as e:
            logging.getLogger('').error('Unexpected error while sending email: {}'.format(str(e)))

    def status_change(self, alert, status, text, **kwargs):
        pass
