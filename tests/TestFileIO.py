"""
Module:  FileIOTests

Description:

This module contains a set of unit tests for the FileIO class.
"""


from log_reader.FileIO import MyFileIO
import os, shutil
import unittest


class TestFileIO(unittest.TestCase):

    def setUp(self):
        """
        All the tidbits needed to set-up for all of the test, such 
        as copy a test file to a tmp directory

        """
        source_file = os.path.join(os.path.abspath(os.path.basename(__file__) + "/../data/"), "log.json")
        self._test_log = os.path.join("/", "tmp", "test.json")
        shutil.copyfile(source_file, self._test_log)


    def tearDown(self):
        """
        All of the clean-up needed once tests have finished.
        """
        os.remove(self._test_log)

    def test_create_instance(self):
        """
        Test creating a File IO ojbect
        """
        test_obj = MyFileIO()
        self.assertNotEqual(test_obj, None, msg="FileIO object was not created.")

        test_obj = MyFileIO("/some_path/some_file")
        self.assertEqual(test_obj.file_path, "/some_path/some_file")
        

    def test_set_properties(self):
        """
        Test setting and getting of the various class properities.
        """
        test_obj = MyFileIO()
        test_obj.file_path = self._test_log
        self.assertEqual(test_obj.file_path, self._test_log, msg="File path is not as expected: " + str(test_obj.file_path))
        self.assertEqual(test_obj.file_name, "test.json", msg="File name is not as expected: " + str(test_obj.file_name))
        self.assertEqual(test_obj.file_ext, ".json", msg="File extension is not as expected: " + str(test_obj.file_ext))
        self.assertEqual(test_obj.file_size, 2891736, msg="File size is not as expected: " + str(test_obj.file_size))  


        # Try setting file path to invalid values
        with self.assertRaises(AssertionError):
            test_obj.file_path = ['/a/path', '/another/path']

        with self.assertRaises(AssertionError):
            test_obj.file_path = 234.234

        with self.assertRaises(AssertionError):
            test_obj.file_path = '/tmp/path/does/not/exist.txt'



        # try setting properties that do not have a setter method
        with self.assertRaises(AssertionError):
            test_obj.file_name = "some name"

        with self.assertRaises(AssertionError):
            test_obj.file_size = 1234


    def test_read_contents(self):
        """
        Test reading the data inside of a file.
        """
        test_obj = MyFileIO()
        test_obj.file_path = self._test_log
        contents = test_obj.get_file_contents()
        self.assertEqual(len(contents), 10000, msg="File was not properly read, " +str(len(contents)) + " was read, 10 000 expected.")

        test_obj.file_path = "/some_bad_file.txt"
        with self.assertRaises(IOError):
            contents = test_obj.get_file_contents()



