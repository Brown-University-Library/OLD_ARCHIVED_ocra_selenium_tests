# -*- coding: utf-8 -*-

import os, re, time, unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class FacultyAddArticleTest( unittest.TestCase ):
    """ Tests adding article. """

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.USERNAME = os.environ.get( 'OCRA_TESTS__FACULTY_USERNAME' )
        self.PASSWORD = os.environ.get( 'OCRA_TESTS__FACULTY_PASSWORD' )
        self.base_url = os.environ.get( 'OCRA_TESTS__FACULTY_START_URL' )
        self.driver.get( self.base_url )
        self.test_course_name = 'BJD_TEST_COURSE'

    ##

    def test_add_article(self):
        """ Checks for required shib login.
            Ensures... """
        driver = self.driver

        # test for Shib
        self.assertTrue( u'sso.brown.edu' in driver.current_url )

        # login
        driver = self._log_into_shib( driver )

        # test we've accessed the main faculty work page
        self.assertTrue( u'reserves/cr/faclogin.php' in driver.current_url )

        # click the manage-my-reserves link
        driver.find_element_by_name("netid").click()

        # test we're at the 'Course Reserves Faculty Interface: Main Menu'
        self.assertTrue( u'reserves/cr/menu.php' in driver.current_url )

        # click the 'Add reserves to a current or upcoming class:' 'Go' button for my 'GRMN 0750E' class
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()

        # test we're at the GRMN 0750E class page
        self.assertTrue( u'reserves/cr/class/?classid=5734' in driver.current_url )

        # test that there's no <table data-restype="article"> element
        self.assertEqual(
            False,
            self._is_css_selector_found( text='table[data-restype="article"]', driver=driver )
            )

        # click the 'View' link for 'Online Readings'
        driver.find_element_by_xpath("(//a[contains(text(),'View')])[2]").click()

        # test that there is a <table data-restype="article"> element
        self.assertEqual(
            True,
            self._is_css_selector_found( text='table[data-restype="article"]', driver=driver )
            )

        # get the article html
        article_html = driver.find_element_by_css_selector( 'table[data-restype="article"]' ).text

        # test that the course to be added is not listed
        self.assertEqual(
            True,
            self.test_course_name not in article_html
            )

        # click the 'Add' link for 'Online Readings'
        driver.find_element_by_xpath("(//a[contains(text(),'Add')])[2]").click()

        # test where we are...



    ##

    def _is_css_selector_found( self, text, driver ):
        """ Helper function to make assert test-statements cleaner. """
        try:
            driver.find_element_by_css_selector( text )
            return True
        except NoSuchElementException as e:
            return False

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
        # self.assertEqual([], self.verificationErrors)



if __name__ == "__main__":
    unittest.main( warnings='ignore' )  # warnings='ignore' from <http://stackoverflow.com/a/21500796>
