# -*- coding: utf-8 -*-

""" Runs `all_tests.py` whenever a git pull is performed,
      and sends email of results.
    Called by `ocra_functional_tests/.git/hooks/post-merge` like...
      source path/to/env/bin/activate
      path/to/env/python path/to/run_tests.py """

import json, os, pprint, smtplib
from email.Header import Header
from email.mime.text import MIMEText
#
import envoy


def run_main():
    """ Calls tests, sends email. """
    ALL_TESTS_PATH = unicode( os.environ.get(u'OCRA_TESTS__ALL_TESTS_PATH') )
    command = u'python %s' % ALL_TESTS_PATH
    r = envoy.run( command.encode(u'utf-8') )  # envoy requires strings
    info = {
        u'std_out': r.std_out.decode(u'utf-8'), u'std_err': r.std_err.decode(u'utf-8'),
        u'status_code': r.status_code,, u'command': r.command, u'history': r.history }
    parsed_info = parse_info( info )
    mailer = Mailer()
    mailer.send_email( parsed_info )
    return


def parse_info( info ):
    """ Checks test output; returns info-dict. """
    return info


class Mailer( object ):
    """ Specs email handling. """

    def __init__(self):
        self.UTF8_RAW_TO = unicode( os.environ.get(u'OCRA_TESTS__MAIL_TO') )  # json (utf-8) string of a list
        self.UTF8_RAW_FROM = unicode( os.environ.get(u'OCRA_TESTS__MAIL_FROM') )  # utf-8 string

    def send_email( parsed_info ):
        """ Sends email. """
        TO = _build_mail_to( self.UTF8_RAW_TO )  # utf-8
        FROM = self.UTF8_RAW_FROM  # utf-8
        SUBJECT = _build_mail_subject( parsed_info )  # unicode
        MESSAGE = json.dumps( parsed_info, sort_keys=True, indent=2 )  # utf-8
        payload = _assemble_payload( TO, FROM, SUBJECT, MESSAGE )
        s = smtplib.SMTP( 'localhost' )
        s.sendmail( FROM, TO, payload.as_string() )
        s.quit()
        return

    def _build_mail_to( UTF8_RAW_TO ):
        """ Builds and returns 'to' list of email addresses.
            Called by send_email() """
        to_emails = json.loads( UTF8_RAW_TO )
        utf8_to_list = []
        for address in to_emails:
            utf8_to_list.append( address.encode('utf-8') )
        return utf8_to_list

    def _build_mail_subject( parsed_info ):
        """ Sets and returns the subject with a success or failure indicator.
            Called by send_email(). """
        unicode_subject = u'subject'
        return unicode_subject

    def _assemble_payload( TO, FROM, SUBJECT, MESSAGE ):
        """ Puts together and returns email payload.
            Called by send_email(). """
        payload = MIMEText( MESSAGE )
        payload['To'] = ', '.join( TO )
        payload['From'] = FROM
        payload['Subject'] = Header( SUBJECT, 'utf-8' )  # SUBJECT must be unicode
        return payload

    # end class Mailer




if __name__ == "__main__":
    run_main()




# import runpy
# runpy.run_module( 'ocra_functional_tests.faculty_add_article_via_details_test' )

# try:
#     execfile( u'/path/to/all_tests.py' )
# except Exception as e:
#     print u'ERROR-----: %s' % unicode( repr(e) )
