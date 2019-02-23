from argparse import ArgumentParser
from argparse import ArgumentTypeError
from datetime import datetime


class Options:

    """
        This class parse arguments.
        - Argument Parser list:
        
        :Options:
            -h --help           Argument parser description 
            --since=<datetime>  Datetime fromdate in format "YYYY-MM-DD" or "YYYY-MM-DD HH:mm
            --until=<datetime>  Datetime todate in format "YYYY-MM-DD" or "YYYY-MM-DD HH:mm
            
            --output-format     json,html
                                Output in format json,html
    """


    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        # construct the argument parse and parse the arguments
        self.parser = ArgumentParser()
        self.parser.add_argument('--stats',
                                 action='store_true',
                                 default=None,
                                 help='Calculates some simple Stackoverflow statistics.')

        self.parser.add_argument('--since',
                                 dest='fromdate',
                                 type=self.valid_date_type,
                                 default=None,
                                 required=False,
                                 help='Datetime in format "YYYY-MM-DD" or "YYYY-MM-DD HH:mm:ss"')

        self.parser.add_argument('--until',
                                 dest='todate',
                                 type=self.valid_date_type,
                                 help='Datetime in format "YYYY-MM-DD" or "YYYY-MM-DD HH:mm:ss"')

        output_params = ['json', 'html', 'tabular']
        self.parser.add_argument('--output-format',
                                 dest='output',
                                 choices=output_params,
                                 help='Output in format json,html"')

    def parse(self, args=None):
        """
        This method  parse args. Returns a Namespace object.Unknown args are ignored and
        parse known args. 
	    Returns (Namespace_of_known, list_of_unknown)

        """

        # parse known args, returns a Namespace object
        # unknown args are ignored
        # Parse known args returns (Namespace_of_known, list_of_unknown)
        #  temp = self.parser.parse_args(args)
        self.known, self.unknown = self.parser.parse_known_args(args)[:]

        if len(self.unknown) != 0:
            raise ValueError(
                '*WARN* Unknown args received: '+repr(self.unknown))

    def valid_date_type(self, arg_date_str):
        """
        This method  parse args_date and raise Value Error if date format is not valid. 
        Datetime it must be in format "YYYY-MM-DD" or "YYYY-MM-DD HH:mm:ss"

        """

        for fmt in ('%Y-%m-%d', '%Y-%m-%d %H:%M:%S'):
            try:
                return datetime.strptime(arg_date_str, fmt)
            except ValueError:
                pass
                msg = "Given Date ({0}) not valid! Expected format, YYYY-MM-DD or YYYY-MM-DD HH:mm:ss ".format(
                    arg_date_str)
        raise ArgumentTypeError(msg)
