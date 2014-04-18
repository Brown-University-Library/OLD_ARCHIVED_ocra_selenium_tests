# -*- coding: utf-8 -*-

import os, re, time, unittest
from selenium import webdriver


class FacultyAddArticleTest( unittest.TestCase ):
    """ Tests adding article. """

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.USERNAME = os.environ.get( 'OCRA_TESTS__FACULTY_USERNAME' )
        self.PASSWORD = os.environ.get( 'OCRA_TESTS__FACULTY_PASSWORD' )
        self.base_url = os.environ.get( 'OCRA_TESTS__FACULTY_START_URL' )
        self.driver.get( self.base_url )

    ##

    # def test_temp(self):
    #     self.assertEqual( 1, 1 )

    ##

    def test_add_article(self):
        """ Checks for required shib login.
            Ensures... """
        driver = self.driver
        # test for Shib
        self.assertTrue( u'sso.brown.edu' in driver.current_url )
        # login
        print( '- driver.current_url BEFORE shib login, %s' % driver.current_url )
        driver = self._log_into_shib( driver )
        # test we've accessed the main faculty work page
        print( '- driver.current_url AFTER shib login, %s' % driver.current_url )
        self.assertTrue( u'reserves/cr/faclogin.php' in driver.current_url )


    # def test_library_staff_login(self):
    #     """ Tests Library Staff login.
    #         Ensures login button brings up shib, then lands on correct page. """
    #     driver = self.driver
    #     # click 'Library Staff Login' button
    #     driver.find_element_by_xpath("//input[@value='Library Staff Login']").click()
    #     # test for Shib
    #     self.assertTrue( u'sso.brown.edu' in driver.current_url )
    #     # login
    #     driver = self._log_into_shib( driver )
    #     # test for lib-staff page
    #     driver.find_element_by_css_selector("button[type=\"submit\"]").click()
    #     self.assertTrue( u'reserves/staff/menu.php' in driver.current_url )

    # def test_itg_staff_login(self):
    #     """ Tests ITG Staff login
    #         Ensures login button brings up shib, then lands on correct page. """
    #     driver = self.driver
    #     # click 'Library Staff Login' button
    #     driver.find_element_by_xpath("//input[@value='ITG Staff Login']").click()
    #     # test for Shib
    #     self.assertTrue( u'sso.brown.edu' in driver.current_url )
    #     # login
    #     driver = self._log_into_shib( driver )
    #     # test for lib-staff page
    #     driver.find_element_by_css_selector("button[type=\"submit\"]").click()
    #     self.assertTrue( u'reserves/staff/menu_itg.php' in driver.current_url )

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
    unittest.main( warnings='ignore' )  # warnings='ignore' from <http://stackoverflow.com/a/21500796>
