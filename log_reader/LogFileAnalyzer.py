"""
Module: FileLogAnalizer

Description:

Analyze the contents of a log file that is in JSON format where each entyr
has the following keys:
   ts:  timestamp
   pt:  processing time
   si:  session ID
   uu:  user UUID
   bg:  business UUID
   sha: sha256 of the file
   nm:  file name
   ph:  path
   dp:  disposition (valid values: MALICIOUS (1), CLEAN (2), UNKNOWN (3))
"""

import os 
from datetime import datetime
import pandas as pd
from log_reader.FileIO import MyFileIO
from log_reader.utilities import StrPattern


class LogFileAnalyzer(object):
    """
    Analyzing the content of a given log file 

    Attributes:
        - data_frame: The data frame that's created from the file.
        - log_file:   Full path to the log file to be examined.
        - valid_keys: dict of expected keys and their
          default is: { "ts":  {"type": datetime, "min": 0, "max": "today", fullname": "timestamp"},
                        "pt":  {"type": float, "min":0,  "fullname": "processing time"},
                        "si":  {"type": RegEx, "pattern": "", "fullname": "Session ID"},
                        "uu":  {"type": RegEx, "pattern": "", "fullname": "User UUID" },
                        "bg":  {"type": RegEx, "pattern": "", "fullname": "Business UUID"}, 
                        "sha": {"type": sha256, "fullname": "sha256 of the file"}, 
                        "nm":  {"type": RegEx, "pattern": "", "fullname": "file name"},
                        "ph":  {"type": str, "min_len": 2, "fullname": "Path to file"},
                        "dp":  {"type": int, values:{1: "MALICIOUS", 2:"CLEAN", 3: "UNKNOWN"}, "fullname": "Dispocition"
                      }
        - log_file:  Full path to the log file to be examined.
    """

    @property
    def log_path(self):
        return self.__log_path
    @log_path.setter
    def log_path(self,value):
        if value is None: self.__log_path=None

        assert isinstance(value,str), "Invalid log_path  given: " + str(value)
        assert os.path.exists(value), "Path provided was not found."
        self.__data_frame = None   # If the log file has change data frame is set back to default
        self.__log_path = value

    @property
    def valid_keys(self):
        return self.__valid_keys
    @valid_keys.setter
    def valid_keys(self,value):
        if value is None: self.__valid_keys=None

        assert isinstance(value,dict), "Invalid valid_key dictionary given: " + str(value)
        self.__valid_keys = value

    @property
    def data_frame(self):
        return self.__data_frame


    def __init__(self, log_path=None, valid_keys=None):
        self.__data_frame = None
        self.__log_path = log_path
        if valid_keys == None:
            uid_pattern = '^([0-9a-fA-F]{8})-([0-9a-fA-F]{4})-([0-9a-fA-F]{4})-([0-9a-fA-F]{4})-([0-9a-fA-F]{12})'
            sha_pattern = '^([0-9a-fA-f]{64})'
            dir_pattern = '^(/[\w.]+)+'
            self.__valid_keys = { "ts":  {"type": datetime, "min": 0, "fullname": "timestamp"},
                        "pt":  {"type": float, "min": 0.0,  "fullname": "processing time"},
                        "si":  {"type": StrPattern, "pattern": uid_pattern, "fullname": "Session ID"},
                        "uu":  {"type": StrPattern, "pattern": uid_pattern, "fullname": "User UUID" },
                        "bg":  {"type": StrPattern, "pattern": uid_pattern, "fullname": "Business UUID"}, 
                        "sha": {"type": StrPattern, "pattern": sha_pattern, "fullname": "sha256 of the file"}, 
                        "nm":  {"type": str, "min_len": 1, "fullname": "file name"},
                        "ph":  {"type": StrPattern, "pattern": dir_pattern, "fullname": "Path to file"},
                        "dp":  {"type": int, "values": {1:"MALICIOUS", 2:"CLEAN", 3:"UNKNOWN"}, "fullname": "Dispocition"},
                      }

    def _validate_row(self, row):
        """
        Validate a row or line of data.
        """
        if self.valid_keys is None:
            # Nothing to do nothing to validate
            return True, ''

        # Check for all of the keys
        if len( set(row.keys()) - set(self.valid_keys.keys())) > 0:
            return False, "extra keys found."
        if len(set(row.keys()) and set(self.valid_keys.keys())) != len(self.valid_keys.keys()):
            return False, "not all keys found."

        for vkey, vvalue in self.valid_keys.items():
            if vvalue['type'] == StrPattern:
                test = StrPattern(pattern=vvalue['pattern'], string=row[vkey])
                if not test.is_match():
                    return False, str(vkey) + ' value "' + str(row[vkey]) + '" does not match expected pattern.'
            elif vvalue['type'] in [int, float]:
                if  vvalue['type'] == int: rvalue = int(row[vkey])
                if  vvalue['type'] == float: rvalue = float(row[vkey])

                if "values" in vvalue.keys() and rvalue not in vvalue['values']:
                    return False, str(vkey) + ' value is "' + str(rvalue) + '" exepcted to be one of ' + str(vvalue['values'])
                if "min" in vvalue.keys() and rvalue<vvalue['min']:
                    return False, str(vkey) + ' value "' + str(rvalue) + '" must be greater than ' + str(vvalue['min'])
                if "max" in vvalue.keys() and rvalue>vvalue['max']:
                    return False, str(vkey) + ' value "' + str(rvalue) + '" must be smaller than ' + str(vvalue['max'])
            elif vvalue['type'] in [str]:
                rvalue = row[vkey]
                if "values" in vvalue.keys() and rvalue not in vvalue['values']:
                    return False, str(vkey) + ' value is "' + str(rvalue) + '" exepcted to be one of ' + str(vvalue['values'])
                if "min_len" in vvalue.keys() and len(rvalue)<vvalue['min_len']:
                    return False, str(vkey) + ' value "' + str(rvalue) + '" must be longer than ' + str(vvalue['min_len']) + ' characters.'
                if "max_len" in vvalue.keys() and len(rvalue)>vvalue['max_len']:
                    return False, str(vkey) + ' value "' + str(rvalue) + '" must be shorter than ' + str(vvalue['max_len']) + ' characters.'
            elif vvalue['type'] is datetime:
                # TODO add the ability to handle things like "today" and "YYYYMMDD" time times
                # TODO print out warning in more meaningful datetime arrangement
                try:
                    # Time is in seconds from epoch
                    seconds = int(row[vkey])
                    rvalue = datetime.fromtimestamp(seconds)
                except:
                     # Time is in YYYY-MM-DD HH:mm:ss format
                     rvalue =  datetime.strptime(row[vkey], "%Y-%m-%d %H:%M:%S")

                if "min" in vvalue.keys() and rvalue < datetime.fromtimestamp(int(vvalue['min'])):
                    return False, str(vkey) + ' value "' + str(rvalue) + '" must be after ' + str(vvalue['min'])
                if "max" in vvalue.keys() and rvalue > datetime.fromtimestamp(int(vvalue['max'])):
                    return False, str(vkey) + ' value "' + str(rvalue) + '" must be before ' + str(vvalue['max'])

            else:
                return False, "Unrecognized value type: " + str(vvalue['type'])

        return True, ''

    def read_and_validate(self):
        """
        Read the contents of the log file and  validate each of the lines of code.

        :return: (int) -- The number of valid rows found in the file.
        """

        my_file = MyFileIO(self.log_path)
        data = my_file.get_file_contents()
        del my_file

        count = 0
        valid_entries=[]
        for line in data:
            count += 1
            if len(line)==0: continue  # Skip blank lines
            line = eval(line)

            # Validate the contents
            ok, err = self._validate_row(line)
            if not ok:
                print('WARNING: line ' + str(count) + ' has failed with ' + err)
                continue

            # Find the file extension
            filename = line['nm']
            root, ext = os.path.splitext(line['nm'])
            line['ext']=ext[1:]

            # If we've reached her line is valid
            valid_entries.append(line)

        
        self.__data_frame = pd.DataFrame(valid_entries)
        return len(self.__data_frame)

    def show_file_type_counts(self):
        """
        Print the number of each type of file found in the log file.

        Note that read_and_validate() must be called before this method
        can be called.
        """
        assert self.__data_frame is not None, "Please call method read_and_validate() first."

        # Use the pandas dataframe to do the counts
        tmp = self.__data_frame.groupby(['ext']).size()
        print(tmp)
        return tmp



