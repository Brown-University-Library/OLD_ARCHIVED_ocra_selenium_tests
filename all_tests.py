# -*- coding: utf-8 -*-

import unittest
from faculty_add_article_via_details_test import FacultyAddArticleViaCitationTest
from faculty_add_article_via_doi_test import FacultyAddArticleViaDoiTest
from home_page_login_test import HomePageLoginTest


def make_suite():
    """ Assembles suite of tests. """
    test_suite = unittest.TestSuite()
    test_suite.addTest( unittest.makeSuite(FacultyAddArticleViaDoiTest) )
    test_suite.addTest( unittest.makeSuite(FacultyAddArticleViaCitationTest) )
    test_suite.addTest( unittest.makeSuite(HomePageLoginTest) )
    return test_suite

full_suite = make_suite()


runner=unittest.TextTestRunner()
runner.run( full_suite )
