# -*- coding: utf-8 -*-

import os, re, time, unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


class HomePageLoginTest( unittest.TestCase ):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://library.brown.edu/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_library_staff_login(self):
        """ Tests Library Staff login """
        # setup
        USERNAME = os.environ.get( u'OCRA__LIBSTAFF_USERNAME' )
        PASSWORD = os.environ.get( u'OCRA__LIBSTAFF_PASSWORD' )
        # access reserves home page
        driver = self.driver
        driver.get(self.base_url + "/reserves/")
        # click 'Library Staff Login' button
        driver.find_element_by_xpath("//input[@value='Library Staff Login']").click()
        # driver.find_element_by_css_selector("#orangebottom > form > input.bodytextSmall").click()  # Library Staff login button
        # test for Shib
        self.assertTrue( u'sso.brown.edu' in driver.current_url )
        # login
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys( USERNAME )
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys( PASSWORD )
        # test for lib-staff page
        driver.find_element_by_css_selector("button[type=\"submit\"]").click()
        self.assertTrue( u'reserves/staff/menu.php' in driver.current_url )

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)




if __name__ == "__main__":
    unittest.main()
