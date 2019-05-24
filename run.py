"""
This is a script to run the code with the sample 
data.
"""

from argparse import ArgumentParser
from log_reader.LogFileAnalyzer import LogFileAnalyzer

def main(log_path):
    """
    Create an instance of the log file analyzer and find out
    what's in it.
    
    Output is to the console
    """

    # TODO capture the warnings and display them optionally.
    lr = LogFileAnalyzer()
    lr.log_path=log_path
    lr.read_and_validate()
    lr.show_file_type_counts()

def parse_args():
    """
    Parse the command-line arguments.
    """

    # TODO allow for showing different type of analytics.
    ap = ArgumentParser('Do analytics on the contents of a logfile.')
    ap.add_argument('-l', '--logfile', action='store', type=str,
                    help='The path to logfile.', required=True)
    args = ap.parse_args()
    return args

if __name__  == '__main__':
    args = parse_args()
    print(args.logfile)
    main(args.logfile)





