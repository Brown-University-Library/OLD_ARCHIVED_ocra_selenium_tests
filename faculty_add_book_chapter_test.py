# -*- coding: utf-8 -*-

import os, pprint, re, time, unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class FacultyBookChapterTest( unittest.TestCase ):
    """ Tests adding a book chapter. """

    def setUp(self):
        """ Initializes and gets us to the add-journal-article page. """
        self.driver = None
        if os.environ.get( 'OCRA_TESTS__DRIVER_TYPE' ) == u'firefox':
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.PhantomJS()
        self.driver.implicitly_wait(30)
        self.USERNAME = os.environ.get( 'OCRA_TESTS__FACULTY_USERNAME' )
        self.PASSWORD = os.environ.get( 'OCRA_TESTS__FACULTY_PASSWORD' )
        self.base_url = os.environ.get( 'OCRA_TESTS__FACULTY_START_URL' )
        self.course_password = os.environ.get( 'OCRA_TESTS__COURSE_PASSWORD' )
        self.driver.get( self.base_url )
        self.test_article_name = 'Seeking God in the Brain — Efforts to Localize Higher Brain Functions'
        self.journal_title = 'New England Journal of Medicine'
        self.article_date = '2008'
        #
        # test for Shib
        self.assertTrue( 'sso.brown.edu' in self.driver.current_url )

        # login
        self.driver = self._log_into_shib( self.driver )

        # test we've accessed the main faculty work page
        self.assertTrue( 'reserves/cr/faclogin.php' in self.driver.current_url )

        # click the manage-my-reserves link
        self.driver.find_element_by_name("netid").click()

        # test we're at the 'Course Reserves Faculty Interface: Main Menu'
        self.assertTrue( 'reserves/cr/menu.php' in self.driver.current_url )

        # click the 'Add reserves to a current or upcoming class:' 'GRMN 0750E' link
        self.driver.find_element_by_link_text("GRMN 0750E: Reading Film: An Introduction to German Cinema").click()

        # test we're at the GRMN 0750E class page
        self.assertTrue( 'reserves/cr/class/?classid=5734' in self.driver.current_url )

        # click the 'Class Details' link to ensure there is a class password set
        self.driver.find_element_by_link_text("Class Details").click()

        # confirm we're at the class edit page
        self.assertTrue( 'reserves/cr/class/edit.php' in self.driver.current_url )

        # confirm the class password (this particular flow assumes a password exists)
        password_element = self.driver.find_element_by_css_selector( 'input[name="password"]' )
        self.assertEqual(
            self.course_password,
            password_element.get_attribute("value") )

        # hit the back button
        self.driver.back()

        # confirm we're back on the x page
        self.assertTrue( 'reserves/cr/class/?classid=5734' in self.driver.current_url )

        # test that there's no <table data-restype="article"> element (no 'Online Readings' view showing)
        self.driver.implicitly_wait(2)  # because I'm asserting False, and it'll wait until the timeout
        self.assertEqual(
            False,
            self._is_css_selector_found( selector_text='table[data-restype="article"]' )
            )
        self.driver.implicitly_wait(30)

        # click the 'View' link for 'Online Readings'
        self.driver.find_element_by_xpath("(//a[contains(text(),'View')])[2]").click()

        # test that there is a <table data-restype="article"> element
        self.assertEqual(
            True,
            self._is_css_selector_found( selector_text='table[data-restype="article"]' )
            )

        # get the article html
        article_html = self.driver.find_element_by_css_selector( 'table[data-restype="article"]' ).text

        # test that the article to be added is not listed
        self.assertEqual(
            True,
            self.test_article_name not in article_html
            )

        # click the 'Add' link for 'Online Readings'
        self.driver.find_element_by_xpath("(//a[contains(text(),'Add')])[2]").click()

        # test that we're on the 'What type of material do you want to add?' page
        self.assertTrue( 'reserves/cr/requestarticle.php' in self.driver.current_url )

    ## test work

    def test_add_book_chapter_or_excerpt(self):
        """ Tests faculty add `Book chapter or excerpt (pdf)` link.
            Note: specified data entered does not trigger auto-find, so that's not tested.
            Tests that:
            - form submit button does not work until required fields are filled out.
            - submitted data exists on subsequent course page.
            """

        driver = self.driver

        # click the `Book chapter or excerpt (pdf)` link
        self.driver.find_element_by_css_selector( u'button.linky[value="excerpt"]' ).click()

        # test we're on the 'Online Readings: Book Excerpt' page
        self.assertEqual(
            True,
            'Online Readings: Book Excerpt' in self.driver.find_element_by_css_selector( 'div#maincontent > h3' ).text
            )

        # test that premature submission yields 'go back' message
        driver.find_element_by_css_selector( u'button' ).click()
        self.assertEqual(
            True,
            u'go back' in self.driver.find_element_by_css_selector( u'p.notice.error' ).text.lower()
            )

        # hit the back button
        self.driver.back()

        # test we're on the 'Online Readings: Book Excerpt' page
        self.assertEqual(
            True,
            'Online Readings: Book Excerpt' in self.driver.find_element_by_css_selector( 'div#maincontent > h3' ).text
            )



    ## helper functions

    def _is_css_selector_found( self, selector_text ):
        """ Helper function to make assert test-statements cleaner. """
        try:
            self.driver.find_element_by_css_selector( selector_text )
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
    unittest.main( verbosity=2, warnings='ignore' )  # warnings='ignore' from <http://stackoverflow.com/a/21500796>
