# -*- coding: utf-8 -*-

import os, pprint, re, time, unittest
import requests
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys


class ApiTest( unittest.TestCase ):
    """ Tests api that A.B. set up to be hit by canvas/ITG folk.
        Note: doesn't use selenium because it's just simpler to use requests for this kind of check. """

    def setUp(self):
        """ Initializes. """
        self.api_base_url = unicode( os.environ.get(u'OCRA_TESTS__API_BASE_URL') )

    ## work

    def test_good_api_call(self):
        """ Tests api, good submission. """
        url = u'%s/COURSE:LITR:0710:2014-Fall:S01:/201410' % self.api_base_url
        r = requests.get( url )
        # print u'url, `%s`' % r.url
        self.assertEqual(
            u'6179',
            r.text )
        self.assertEqual(
            200,
            r.status_code )

    def test_ocra_course_missing(self):
        """ Tests api, grouper-course w/o ocra entry. """
        url = u'%s/COURSE:AFRI:1700C:2014-Fall:S01/201410' % self.api_base_url
        r = requests.get( url )
        # print u'url, `%s`' % r.url
        self.assertEqual(
            u'',
            r.text )
        self.assertEqual(
            404,
            r.status_code )

    ##

    def tearDown(self):
        pass



if __name__ == "__main__":
    # print u'about to run test'
    runner = unittest.TextTestRunner( verbosity=2 )
    unittest.main( testRunner=runner )  # python2
    # print u'test done'
    # unittest.main( verbosity=2, warnings='ignore' )  # python3; warnings='ignore' from <http://stackoverflow.com/a/21500796>
