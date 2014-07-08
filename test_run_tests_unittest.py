# -*- coding: utf-8 -*-

""" Unit-tests run_tests.py """

import json, os, pprint, re, time, unittest
import run_tests


class RunTestsTest( unittest.TestCase ):

    def test_parse_info__single_success( self ):
        json_string = u'''{
          "command": [
            "python",
            "/path/to/faculty_add_article_via_details_test.py"
          ],
          "history": [],
          "status_code": 0,
          "std_err": "Tests faculty add-article via details method. ... ok\\n\\n----------------------------------------------------------------------\\nRan 1 test in 19.885s\\n\\nOK\\n",
          "std_out": ""
        }'''
        info_dict = json.loads( json_string )
        assert type(info_dict) == dict
        result_dict = run_tests.parse_info( info_dict )
        self.assertEqual(
            [u'message', u'subject'],
            sorted( result_dict.keys() )
            )
        self.assertEqual(
            u'ocra interface-tests passed',
            result_dict[u'subject']
            )
        self.assertEqual(
            u'tests output...\n\n' + info_dict[u'std_err'],
            result_dict[u'message']
            )

    def test_parse_info__single_failure( self ):
        json_string = u'''{
          "command": [
            "python",
            "/path/to/faculty_add_article_via_details_test.py"
          ],
          "history": [],
          "status_code": 1,
          "std_err": "Tests faculty add-article via details method. ... ERROR\\n\\n======================================================================\\nERROR: Tests faculty add-article via details method.\\n----------------------------------------------------------------------\\nTraceback (most recent call last):\\n  File \\"/path/to/faculty_add_article_via_details_test.py\\", line 38, in setUp\\n    self.assertTrue( 'reserves/cr/test_bad_url.php' in self.driver.current_url )\\nAssertionError\\n\\n----------------------------------------------------------------------\\nRan 1 test in 6.249s\\n\\nFAILED (errors=1)\\n",
          "std_out": ""
        }'''
        info_dict = json.loads( json_string )
        assert type(info_dict) == dict
        result_dict = run_tests.parse_info( info_dict )
        self.assertEqual(
            [u'message', u'subject'],
            sorted( result_dict.keys() )
            )
        self.assertEqual(
            u'ocra interface-tests PROBLEM',
            result_dict[u'subject']
            )
        self.assertEqual(
            u'tests output...\n\n' + info_dict[u'std_err'],
            result_dict[u'message']
            )

    def test_parse_info__success_and_failure( self ):
        json_string = u'''{
          "command": [
            "python",
            "/path/to/all_tests.py"
          ],
          "history": [],
          "status_code": 0,
          "std_err": "Tests faculty add-article via details method. ... ERROR\\nTests faculty add-article via detail method. ... ok\\nTests faculty add `Book chapter or excerpt (pdf)` link. ... ok\\nTests ITG Staff login. ... ok\\nTests Library Staff login. ... ok\\n\\n======================================================================\\nERROR: Tests faculty add-article via details method.\\n----------------------------------------------------------------------\\nTraceback (most recent call last):\\n  File \\"/path/to/faculty_add_article_via_details_test.py\\", line 38, in setUp\\n    self.assertTrue( 'reserves/cr/faclogin.phpzz' in self.driver.current_url )\\nAssertionError\\n\\n----------------------------------------------------------------------\\nRan 5 tests in 45.867s\\n\\nFAILED (errors=1)\\n",
          "std_out": "DOI found\\ntime-taken: 0:00:45.867067\\n"
        }'''
        info_dict = json.loads( json_string )
        assert type(info_dict) == dict
        result_dict = run_tests.parse_info( info_dict )
        self.assertEqual(
            [u'message', u'subject'],
            sorted( result_dict.keys() )
            )
        self.assertEqual(
            u'ocra interface-tests PROBLEM',
            result_dict[u'subject']
            )
        self.assertEqual(
            u'tests output...\n\n' + info_dict[u'std_err'],
            result_dict[u'message']
            )




if __name__ == "__main__":
    runner = unittest.TextTestRunner( verbosity=2 )
    unittest.main( testRunner=runner )  # python2
