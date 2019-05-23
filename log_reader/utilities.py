"""
Module: MyTypes

Description:

This module contains the definition of a number of custome types
"""

import re

class StrPattern(object):
    """
    A class for handling strings that must match a regular expression

    Attributues:
       - string:  The string that is expected to match the regular expression
       - pattern: The regular expression that the string is to match
    """

    @property
    def string(self):
       return self.__string
    @string.setter
    def string(self, value):
        if value is None: self.__string = None; return
        assert isinstance(value,str), "Invalid value given for str property: " + str(value)
        self.__string=value

    @property
    def pattern(self):
       return self.__pattern
    @pattern.setter
    def pattern(self, value):
        if value is None: self.__pattern = None; return
        assert isinstance(value,str), "Invalid value given for pattern property: " + str(value)
        self.__pattern=value


    def __init__(self, pattern=None, string=None):
        self.pattern=pattern
        self.string=string

    def is_match(self):
        match = re.match(self.pattern, self.string)
        return match is not None
