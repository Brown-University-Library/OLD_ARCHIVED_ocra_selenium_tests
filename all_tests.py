# -*- coding: utf-8 -*-

import unittest
from faculty_add_article_tests import FacultyAddArticleTest
from home_page_login_tests import HomePageLoginTest


def make_suite():
    """ Assembles suite of tests. """
    test_suite = unittest.TestSuite()
    test_suite.addTest( unittest.makeSuite(FacultyAddArticleTest) )
    test_suite.addTest( unittest.makeSuite(HomePageLoginTest) )
    return test_suite

full_suite = make_suite()


runner=unittest.TextTestRunner()
runner.run( full_suite )
