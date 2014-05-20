# -*- coding: utf-8 -*-

import os, re, sys, time, unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class FacultyAddArticleViaDoiTest( unittest.TestCase ):
    """ Tests adding article. """

    def setUp(self):
        self.driver = None
        if os.environ.get( u'OCRA_TESTS__DRIVER_TYPE' ) == u'firefox':
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.PhantomJS( u'%s' % driver_type )  # will be path to phantomjs
        self.driver.implicitly_wait(30)
        self.USERNAME = unicode( os.environ.get( u'OCRA_TESTS__FACULTY_USERNAME' ) )
        self.PASSWORD = unicode( os.environ.get( u'OCRA_TESTS__FACULTY_PASSWORD' ) )
        self.base_url = unicode( os.environ.get( u'OCRA_TESTS__FACULTY_START_URL' ) )
        self.driver.get( self.base_url )
        self.test_article_name = u'Seeking God in the Brain — Efforts to Localize Higher Brain Functions'
        self.test_article_doi = u'doi:10.1056/NEJMp078206'

    ##

    def test_add_article_via_doi(self):
        """ Tests faculty add-article via detail method.
            Note: specified -- good -- DOI is sometimes found and not-found.
            Tests that:
            - both found and not-found paths work as expected.
            - submitted data exists on subsequent course page.
            """
        driver = self.driver

        # test for Shib
        self.assertTrue( 'sso.brown.edu' in driver.current_url )

        # login
        driver = self._log_into_shib( driver )

        # test we've accessed the main faculty work page
        self.assertTrue( 'reserves/cr/faclogin.php' in driver.current_url )

        # click the manage-my-reserves link
        driver.find_element_by_name("netid").click()

        # test we're at the 'Course Reserves Faculty Interface: Main Menu'
        self.assertTrue( 'reserves/cr/menu.php' in driver.current_url )

        # click the 'Add reserves to a current or upcoming class:' 'GRMN 0750E' link
        driver.find_element_by_link_text("GRMN 0750E: Reading Film: An Introduction to German Cinema").click()
        # driver.find_element_by_css_selector("input[type=\"submit\"]").click()

        # test we're at the GRMN 0750E class page
        self.assertTrue( 'reserves/cr/class/?classid=5734' in driver.current_url )

        # test that there's no <table data-restype="article"> element
        driver.implicitly_wait(2)  # because I'm asserting False, and it'll wait until the timeout
        self.assertEqual(
            False,
            self._is_css_selector_found( selector_text='table[data-restype="article"]' )
            )
        driver.implicitly_wait(30)

        # click the 'View' link for 'Online Readings'
        driver.find_element_by_xpath("(//a[contains(text(),'View')])[2]").click()

        # test that there is a <table data-restype="article"> element
        self.assertEqual(
            True,
            self._is_css_selector_found( selector_text='table[data-restype="article"]' )
            )

        # get the article html
        article_html = driver.find_element_by_css_selector( 'table[data-restype="article"]' ).text

        # test that the article to be added is not listed
        self.assertEqual(
            True,
            self.test_article_name not in article_html
            )

        # click the 'Add' link for 'Online Readings'
        driver.find_element_by_xpath("(//a[contains(text(),'Add')])[2]").click()

        # test that we're on the 'What type of material do you want to add?' page
        self.assertTrue( 'reserves/cr/requestarticle.php' in driver.current_url )

        # click the 'Journal Article link'
        driver.find_element_by_name("subtask").click()

        # test we're on the 'Enter Journal Article Citation' page
        self.assertEqual(
            True,
            'Enter Journal Article Citation' in driver.find_element_by_css_selector( 'div#maincontent > h3' ).text
            )

        # option 1 -- fill out doi & submit
        driver.find_element_by_id("_doi").clear()
        driver.find_element_by_id("_doi").send_keys("doi:10.1056/NEJMp078206")
        driver.find_element_by_id("lookupByID").click()

        # check whether the doi was found
        sleep_counter = 1
        doi_found = False
        while sleep_counter < 15:
            time.sleep( sleep_counter )
            driver.implicitly_wait( 1 )
            try:
                # confirm it found an article
                article_citation_html = driver.find_element_by_css_selector( 'blockquote > p' ).text
                self.assertEqual(
                    True,
                    self.test_article_name in article_citation_html
                    )
                print( 'DOI found' )
                doi_found = True
                driver.implicitly_wait( 30 )
                break
            except Exception as e:
                sleep_counter += 5
                print( 'DOI not found; sleep_counter, %s' % sleep_counter )
                pass

        # stop test if no doi found
        if not doi_found:
            print( 'NOTE: No DOI found; aborting rest of DOI test.' )
            return

        ## getting here means the doi was found ##

        # request article, _not_ filling out any of the info in the red at the bottom
        driver.find_element_by_css_selector("#citVerify > form > button[type=\"submit\"]").click()

        # confirm success via url
        self.assertTrue( 'reserves/cr/class/?classid=5734&success' in driver.current_url )

        # confirm confirmation box on page
        confirmation_html = article_citation_html = driver.find_element_by_css_selector( 'p.notice.success' ).text
        self.assertEqual(
            True,
            self.test_article_name in confirmation_html
            )

        # click the 'View' link for 'Online Readings'
        driver.find_element_by_xpath("(//a[contains(text(),'View')])[2]").click()

        # get the article html
        article_html = driver.find_element_by_css_selector( 'table[data-restype="article"]' ).text

        # test that the added article is listed
        self.assertEqual(
            True,
            self.test_article_name in article_html
            )

        # determine delete link
        article_table_element = driver.find_element_by_css_selector( 'div#articles > table > tbody' )
        table_rows = article_table_element.find_elements_by_tag_name( 'tr' )
        target_row_counter = 1  # because xpath call is 1-indexed, not zero-indexed
        for row in table_rows:
            if self.test_article_name in row.text:
                break
            else:
                target_row_counter += 1
        # print( '- TARGET ROW COUNTER, %s' % target_row_counter )

        # click the delete link
        driver.find_element_by_xpath( "(//a[contains(text(),'Delete')])[%s]" % target_row_counter ).click()

        # test that the added article is no longer listed
        time.sleep( 1 )  # needed; an immediate check will still show the text of the deleted citation
        article_html = driver.find_element_by_css_selector( 'table[data-restype="article"]' ).text
        self.assertTrue( self.test_article_name not in article_html )

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
    runner = unittest.TextTestRunner( verbosity=2 )
    unittest.main( testRunner=runner )  # python2
    # unittest.main( verbosity=2, warnings='ignore' )  # python3; warnings='ignore' from <http://stackoverflow.com/a/21500796>
