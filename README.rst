=============
Log Reader
=============

Public Code Sample
-------------------
The main purpose of this code sample is an example of what I developed for a coding exercise. 
The code itself was done in a couple of days, is by no means complete although I might tinker
at it in the future.  

The instructions giving to me for the exercise are below.

The pandas library was choosen to do the analytics, although it is not really needed for the
excercise as it was described.  It was choosen because with it, it would be easy to do many
other analytics on the data in the log file.

Assumptions that were made:

-   "ts" field is in too different formats as follows:
    
     1. an integer representing the number of seconds since the epoch
     2. a string in the format YYYY-MM-DD HH:mm:ss

-   All IDs, whether they are session, user or others are set of hex values with sizes
    8 - 4 - 4 - 4 - 12 

-   The sha256 hash values of the files are 64 characters long

-   "ph" path field is a path, no filenames allowed and they are unix file system paths.


Installation
-------------------
The steps are as follows:

1. Get a copy of the software
   git clone https://github.com/geeklady2/log_reader.git

2. Install the pandas software with pip 
   pip install pandas

3. Install on your system, this step is not necessarcy for
   using and testing.
   python setup install  


Usage
-------------------
The software has been tested with Python 2.7 and 3.6, it should work with other 
versions as well.

Type the command below in the directory where the software was copied 

python run --logfile <path to log file>


Testing
--------------------
The easiest way to run the tests is to use the python nose package and run
it to run the tests as follows:

1. pip install nose

2. nosetests
   nosetests --nocapture   (use this command to see the output commands in the tests)

Note that two of the test are expected to fail as the StrPattern class
does not verify that the pattern value is a valid regular expression and
MyFileIO does not check if the file exists when file_path is set.  This
could be considered ok behaviour, it might be better if it errors 
earlier rather then later though when these values are being used.

Original Request
---------------------
 The orignal request and problem that this software addresses is
 the following scenario
    
We have a fictitious log file of JSON data that gives us information on files that were seen by users and whether it is safe or not (disposition).   This log file is in data/log.json in the software repository.
    
JSON format:
    ts:  timestamp
    pt:  processing time
    si:  session ID
    uu:  user UUID
    bg:  business UUID
    sha: sha256 of the file
    nm:  file name
    ph:  path
    dp:  disposition (valid values: MALICIOUS (1), CLEAN (2), UNKNOWN (3))
    
    We would expect the output:
    ext: 1
    pdf: 1


    Example file data

{"ts":1551140352,"pt":55,"si":"3380fb19-0bdb-46ab-8781-e4c5cd448074","uu":"0dd24034-36d6-4b1e-a6c1-a52cc984f105","bg":"77e28e28-745a-474b-a496-3c0e086eaec0","
sha":"abb3ec1b8174043d5cd21d21fbe3c3fb3e9a11c7ceff3314a3222404feedda52","nm":"phkkrw.ext","ph":"/efvrfutgp/expgh/phkkrw","dp":2}
{"ts":1551140352,"pt":55,"si":"3380fb19-0bdb-46ab-8781-e4c5cd448074","uu":"0dd24034-36d6-4b1e-a6c1-a52cc984f105","bg":"77e28e28-745a-474b-a496-3c0e086eaec0","
sha":"abb3ec1b8174043d5cd21d21fbe3c3fb3e9a11c7ceff3314a3222404feedda52","nm":"asdf.pdf","ph":"/efvrfutgp/asdf.pdf","dp":2}
{"ts":1551140352,"pt":55,"si":"3380fb19-0bdb-46ab-8781-e4c5cd448074","uu":"0dd24034-36d6-4b1e-a6c1-a52cc984f105","bg":"77e28e28-745a-474b-a496-3c0e086eaec0","
sha":"abb3ec1b8174043d5cd21d21fbe3c3fb3e9a11c7ceff3314a3222404feedda52","nm":"phkkrw.ext","ph":"/efvrfutgp/expgh/phkkrw","dp":2}
