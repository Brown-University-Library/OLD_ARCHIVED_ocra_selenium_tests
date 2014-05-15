# -*- coding: utf-8 -*-

import os, re, time, unittest
from selenium import webdriver


class HomePageLoginTest( unittest.TestCase ):
    """ Tests home-page login buttons. """

    def setUp(self):
        self.driver = None
        driver_type = unicode( os.environ.get('OCRA_TESTS__DRIVER_TYPE') )
        if driver_type == u'firefox':
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.PhantomJS( u'%s' % driver_type )  # will be path to phantomjs
        self.driver.implicitly_wait(30)
        self.base_url = os.environ.get( 'OCRA_TESTS__LOGIN_BASE_URL' )
        self.USERNAME = os.environ.get( 'OCRA_TESTS__LIBSTAFF_USERNAME' )
        self.PASSWORD = os.environ.get( 'OCRA_TESTS__LIBSTAFF_PASSWORD' )
        # access reserves home page
        self.driver.get(self.base_url + "/reserves/")

    # def setUp(self):
    #     self.driver = None
    #     if os.environ.get( 'OCRA_TESTS__DRIVER_TYPE' ) == u'firefox':
    #         self.driver = webdriver.Firefox()
    #     else:
    #         self.driver = webdriver.PhantomJS()
    #     self.driver.implicitly_wait(30)
    #     self.base_url = os.environ.get( 'OCRA_TESTS__LOGIN_BASE_URL' )
    #     self.USERNAME = os.environ.get( 'OCRA_TESTS__LIBSTAFF_USERNAME' )
    #     self.PASSWORD = os.environ.get( 'OCRA_TESTS__LIBSTAFF_PASSWORD' )
    #     # access reserves home page
    #     self.driver.get(self.base_url + "/reserves/")

    ##

    def test_library_staff_login(self):
        """ Tests Library Staff login.
            Ensures login button brings up shib, then lands on correct page. """
        driver = self.driver
        # click 'Library Staff Login' button
        driver.find_element_by_xpath("//input[@value='Library Staff Login']").click()
        # test for Shib
        self.assertTrue( u'sso.brown.edu' in driver.current_url )
        # login
        driver = self._log_into_shib( driver )
        # test for lib-staff page
        self.assertTrue( u'reserves/staff/menu.php' in driver.current_url )

    def test_itg_staff_login(self):
        """ Tests ITG Staff login.
            Ensures login button brings up shib, then lands on correct page. """
        driver = self.driver
        # click 'Library Staff Login' button
        driver.find_element_by_xpath("//input[@value='ITG Staff Login']").click()
        # test for Shib
        self.assertTrue( u'sso.brown.edu' in driver.current_url )
        # login
        driver = self._log_into_shib( driver )
        # test for lib-staff page
        self.assertTrue( u'reserves/staff/menu_itg.php' in driver.current_url )

    def _log_into_shib( self, driver ):
        """ Helper function for tests.
            Takes driver; logs in user; returns driver.
            Called by module test functions. """
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys( self.USERNAME )
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys( self.PASSWORD )
        driver.find_element_by_css_selector("button[type=\"submit\"]").click()
        return driver

    ##

    def tearDown(self):
        self.driver.quit()




if __name__ == "__main__":
    runner = unittest.TextTestRunner( verbosity=2 )
    unittest.main( testRunner=runner )  # python2
    # unittest.main( verbosity=2, warnings='ignore' )  # python3; warnings='ignore' from <http://stackoverflow.com/a/21500796>
