# -*- coding: utf-8 -*-

import os, pprint, re, time, unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


class FacultyAddArticleViaCitationTest( unittest.TestCase ):
    """ Tests adding article via detail method. """

    def setUp(self):
        """ Initializes and gets us to the add-journal-article page. """
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.USERNAME = os.environ.get( 'OCRA_TESTS__FACULTY_USERNAME' )
        self.PASSWORD = os.environ.get( 'OCRA_TESTS__FACULTY_PASSWORD' )
        self.base_url = os.environ.get( 'OCRA_TESTS__FACULTY_START_URL' )
        self.driver.get( self.base_url )
        self.test_article_name = 'Seeking God in the Brain — Efforts to Localize Higher Brain Functions'
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

        # test that there's no <table data-restype="article"> element
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

        # click the 'Journal Article link'
        self.driver.find_element_by_name("subtask").click()

        # test we're on the 'Enter Journal Article Citation' page
        self.assertEqual(
            True,
            'Enter Journal Article Citation' in self.driver.find_element_by_css_selector( 'div#maincontent > h3' ).text
            )

    ## work

    def test_add_article_via_details(self):
        """ Tests adding article via detail method. """

        driver = self.driver

        # confirm the 'details search' view is not shown
        details_element = driver.find_element_by_css_selector( 'div#articleDetails' )
        self.assertEqual(
            False,
            details_element.is_displayed() )

        # click option 3: 'Enter article details'
        driver.find_element_by_id("ui-accordion-artcit-header-2").click()

        # confirm the 'details search' view is shown
        time.sleep( 1 )
        details_element = driver.find_element_by_css_selector( 'div#articleDetails' )
        self.assertEqual(
            True,
            details_element.is_displayed() )

        # confirm the button is clickable
        button_element = driver.find_element_by_id("details_submit_button")
        self.assertEqual(
            '',
            button_element.get_attribute( 'class' ) )

        # confirm no button-triggered tooltips
        button_element = driver.find_element_by_id("details_submit_button")
        self.assertEqual(
            None,
            button_element.get_attribute('aria-describedby') )
        # print( 'aria-describedby before, %s' % button_element.get_attribute('aria-describedby') )

        # hover over the submit button
        button_element = driver.find_element_by_id("details_submit_button")
        hover = ActionChains(driver).move_to_element(button_element)
        hover.perform()

        # confirm the button-triggered tooltips
        # button_element = driver.find_element_by_id("details_submit_button")
        self.assertEqual(
            'ui-tooltip-0',
            button_element.get_attribute('aria-describedby') )
        # print( 'aria-describedby after hover, %s' % button_element.get_attribute('aria-describedby') )

        # confirm the button is disabled
        self.assertEqual(
            'disabled',
            button_element.get_attribute( 'class' ) )

        # try to click submit anyway, without filling in required fields
        driver.find_element_by_id( 'details_submit_button' ).click()

        # confirm we're still on the same page
        self.assertTrue( 'reserves/cr/requestarticle.php' in self.driver.current_url )

        # confirm the 'details search' view is still shown
        details_element = driver.find_element_by_css_selector( 'div#articleDetails' )
        self.assertEqual(
            True,
            details_element.is_displayed() )


        1/0





        # # option 1 -- fill out doi & submit
        # driver.find_element_by_id("_doi").clear()
        # driver.find_element_by_id("_doi").send_keys("doi:10.1056/NEJMp078206")
        # driver.find_element_by_id("lookupByID").click()

        # # confirm it found an article
        # article_citation_html = driver.find_element_by_css_selector( 'blockquote > p' ).text
        # self.assertEqual(
        #     True,
        #     self.test_article_name in article_citation_html
        #     )

        # # request it, _not_ filling out any of the info in the red at the bottom
        # driver.find_element_by_css_selector("#citVerify > form > button[type=\"submit\"]").click()

        # # confirm success via url
        # self.assertTrue( 'reserves/cr/class/?classid=5734&success' in driver.current_url )

        # # confirm confirmation box on page
        # confirmation_html = article_citation_html = driver.find_element_by_css_selector( 'p.notice.success' ).text
        # self.assertEqual(
        #     True,
        #     self.test_article_name in confirmation_html
        #     )

        # # click the 'View' link for 'Online Readings'
        # driver.find_element_by_xpath("(//a[contains(text(),'View')])[2]").click()

        # # get the article html
        # article_html = driver.find_element_by_css_selector( 'table[data-restype="article"]' ).text

        # # test that the added article is listed
        # self.assertEqual(
        #     True,
        #     self.test_article_name in article_html
        #     )

        # # determine delete link
        # article_table_element = driver.find_element_by_css_selector( 'div#articles > table > tbody' )
        # table_rows = article_table_element.find_elements_by_tag_name( 'tr' )
        # target_row_counter = 1  # because xpath call is 1-indexed, not zero-indexed
        # for row in table_rows:
        #     if self.test_article_name in row.text:
        #         break
        #     else:
        #         target_row_counter += 1
        # # print( '- TARGET ROW COUNTER, %s' % target_row_counter )

        # # click the delete link
        # driver.find_element_by_xpath( "(//a[contains(text(),'Delete')])[%s]" % target_row_counter ).click()

        # # test that the added article is no longer listed
        # time.sleep( 1 )  # needed; an immediate check will still show the text of the deleted citation
        # article_html = driver.find_element_by_css_selector( 'table[data-restype="article"]' ).text
        # self.assertTrue( self.test_article_name not in article_html )

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
    unittest.main( warnings='ignore' )  # warnings='ignore' from <http://stackoverflow.com/a/21500796>
