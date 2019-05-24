"""
Module: FileIO

Description:

This module handles reading and writing of files.


Todo:
  - Add write features
  - Support binary files
  - Add the ability to us checksums to verify content.
  - Add support for compression/decompression
"""

import os

class MyFileIO(object):
    """
    A class that handle reading and writing files.

    Attributes:
      - file_path:  Fully specified path to the file to be read or written
      - file_name:  The "name" portion of the file
      - file_ext:   The "ext" of the file, example jpg for my_image.jpg
      - file_size:  How big the file is in bytes.
    """

    @property
    def file_path(self):
        return self.__file_path
    @file_path.setter
    def file_path(self, value):
        if value is None: self.__file_path = None; return
        assert isinstance(value, str), "Invalid file path given"
        self.__file_path = value


    @property
    def file_name(self):
        if self.file_path != None:
            return os.path.basename(self.file_path)
        return None

    @property
    def file_ext(self):
        if self.file_path != None:
            root, ext = os.path.splitext(self.file_path)
            return ext
        return None

    @property
    def file_size(self):
        if self.file_path != None:
            return os.path.getsize(self.file_path)
        return -1


    def __init__(self, file_path=None):
        self.file_path = file_path
   
    def get_file_contents(self):
        """
        Read the contents of a file.

        :return: (list of str) - Each item in the list is a line in the file.
        """
        data = []
        with open(self.file_path, 'r') as fp:
            data = fp.readlines()

        return data
    
    
    
 



