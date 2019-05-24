"""
Test: LogFileAnalyzer

Description:

Test the LogFileAnalyzer class.
"""

import os, shutil
import unittest
import pandas
from log_reader.LogFileAnalyzer import LogFileAnalyzer

class TestLogFileAnalyzer(unittest.TestCase):

    def setUp(self):
        """
        Set-up for all of the test, such as copy a test file to a tmp directory

        """
        source_file = os.path.join(os.path.abspath(os.path.basename(__file__) + "/../data/"), "log.json")
        self._test_log = os.path.join("/", "tmp", "test.json")
        shutil.copyfile(source_file, self._test_log)

        path = os.path.join('/', 'tmp', 'somefile.txt')
        with open(path, 'a'):
            os.utime(path, None)


    def tearDown(self):
        """
        All of the clean-up needed once tests have finished.
        """
        os.remove(self._test_log)

    def test_create_instance(self):
        test = LogFileAnalyzer()
        self.assertEqual(test.data_frame, None, msg="Initialized Log Analyzyer does not have a null data frame.")
        self.assertEqual(test.log_path, None, msg="Initialized Log Analyzyer does not have a null log file.")
        self.assertEqual(set(test.valid_keys.keys()), set(["ts", "pt", "si", "uu", "bg", "sha", "nm", "ph", "dp"]),
               msg="Initialized Log Analyzyer is not the default valid key dictionary .")


        test = LogFileAnalyzer(log_path=self._test_log)
        self.assertEqual(test.data_frame, None, msg="Initialized Log Analyzyer does not have a null data frame.")
        self.assertEqual(test.log_path, self._test_log, msg="Initialized Log Analyzyer is not the test log.")
        test.valid_keys=None
        self.assertEqual(test.valid_keys, None,
               msg="Initialized Log Analyzyer does not have a null valid key dictionary .")   

    def test_set_properties(self):
        """
        Test setting the properties of the class.
        """
        test = LogFileAnalyzer()

        # Test valid values
        test_path = os.path.join('/', 'tmp', 'somefile.txt')
        test.log_path=test_path
        self.assertEqual(test.log_path, test_path, msg="log path was not set properly.")

        test_keys = {"a": int, "b": str, "c": str, "d": list}
        test.valid_keys=test_keys
        self.assertEqual(test.valid_keys, test_keys, msg="valid keys was not set properly.")
        
  
        # Test invalid log path values
        test = LogFileAnalyzer()
        with self.assertRaises(AssertionError):
            test.log_path = 9
        with self.assertRaises(AssertionError):
        	test.log_path = os.path.join('/', 'bad_dir', 'bad_file.txt')
        with self.assertRaises(AssertionError):
        	test.log_path = pandas.DataFrame()
  
        # Test invalid valid key values
        with self.assertRaises(AssertionError):
        	test.valid_keys = 234.234
        with self.assertRaises(AssertionError):
        	test.valid_keys = [1,2,3,4,5]

        # Try and set data frame which is not allowed
        df = pandas.DataFrame()
        with self.assertRaises(AttributeError):
            test.data_frame=df


    def test_reading_a_file(self):
    	"""
    	Do test on reading the data from a file and validating it.
    	"""
        # Read a file with 9985 valid records in it.
        # The invalid ones that were reported have at least one field
        # that does not match the expected values we've used in the
        # example.
    	test = LogFileAnalyzer(log_path=self._test_log)
    	num_valid_records = test.read_and_validate()
        self.assertEqual(num_valid_records, 9985, msg='The wrong number of valid records were found in the test file.')

        # TODO test with a number of bad files

    def test_show_ext_coung(self):
        """
        Do tests on the function that shows the file extensions.
        """
        test = LogFileAnalyzer(log_path=self._test_log)

        # This is an error, the file must be read and validated first.
        with self.assertRaises(AssertionError):
            test.show_file_type_counts()
        
        # The results are Based on findings used with grep manually
        # TODO would be to keep track of the invalid entries so that
        # grep usage coule be automated.
        test.read_and_validate()
        df = test.show_file_type_counts()
        self.assertEqual(208, df['class'], msg="Number of .class files found differs.")
        self.assertEqual(174, df['mid'], msg="Number of .mid files found differs.")
        self.assertEqual(155, df['xls'], msg="Number of .xls files found differs.")
        self.assertEqual(9985, df.sum(), msg="Sum of all the counts is not equal to number of valid records.")
 
        # TODO test with a number of different bad files