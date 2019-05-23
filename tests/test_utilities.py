"""
Module:  TestUtilities

Description:

Test any of the utility functions and or classes.
"""

import unittest
from log_reader.utilities import StrPattern

class TestStrPattern(unittest.TestCase):

    def setUp(self):
    	"""No setUp needed at this point."""
    	pass
    def tearDown(self):
    	"""No tear down needed at this point"""
    	pass

    def test_create_class(self):
    	test = StrPattern()
    	self.assertIsNotNone(test, "Create failed")

    def test_set_properties(self):
    	test = StrPattern()

    	# Set with valid properties
    	test.string = 'lorem ipsum'
    	self.assertEqual(test.string, 'lorem ipsum', msg="Failed to set StrPattern string property.")
    	test.pattern = '[\w.]+@[\w]+'
    	self.assertEqual(test.pattern, '[\w.]+@[\w]+', msg='Failed to set StrPattern pattern property')

    	# Test invalid string property values
        with self.assertRaises(AssertionError):
        	test.string=9 
        with self.assertRaises(AssertionError):	
    		test.string=['a', 'b', 'c']

    	# Test invalid pattern property values
        with self.assertRaises(AssertionError):
    		test.pattern='some random string that is not a regular expression'

        with self.assertRaises(AssertionError):
    		test.pattern=2.3

        with self.assertRaises(AssertionError):
    		test.pattern={'a': 1, 'b': 2, }


    def test_uuid(self):
    	"""Test strings matching a user ID"""

    	uuid = StrPattern(pattern = r'^([0-9a-fA-F]{8})-([0-9a-fA-F]{4})-([0-9a-fA-F]{4})-([0-9a-fA-F]{4})-([0-9a-fA-F]{12})')

        # A valid string all lower case
    	uuid.string = '43653c2c-ebca-46a2-8678-acd4b171d175'
    	self.assertTrue(uuid.is_match(), 
    		      msg='input "43653c2c-ebca-46a2-8678-acd4b171d175" was expected to match but does not.')

        # A valid string with mixed case
        uuid.string='8214ebed-a31b-477F-Ac5d-cd35fb04b810'
        self.assertTrue(uuid.is_match(), 
    		      msg='input "8214ebed-a31b-477F-Ac5d-cd35fb04b810" was expected to match but does not.')

        # A valid string with upper case
        uuid.string='43653C2C-EBCA-46A2-8678-ACD4B171D175'
        self.assertTrue(uuid.is_match(), 
    		      msg='input "43653C2C-EBCA-46A2-8678-ACD4B171D175" was expected to match but does not.')


        # Try some invalid values
        with self.assertRaises(AssertionError):
        	uuid.string = -987

        with self.assertRaises(AssertionError):
            uuid.string = {}

                    


