import sys
from lib import stackstats
from lib import Options
from lib import stacks
import json


def main():
    """
        This method called with command-line executable. Use sys.arguments
        Create an object options to check if arguments are valid, if not a
        ValuError caused. If one of the arguments is --stats an
        stackstats object is created and calculate the application assignment.

        Argument Parser list :

        :Usage (Examples):
            stacks --stats --since '2016-06-02 10:00:00', --until '2016-06-02 11:00:00' --output-format json
            stacks --stats --since '2016-02-10'
            stacks --stats --until '2016-02-10 10:30:00' --output-format json
            stacks (-h | --help)

        :Options:
            -h --help           Argument parser description 
            --since=<datetime>  Datetime fromdate in format "YYYY-MM-DD" or "YYYY-MM-DD HH:mm
            --until=<datetime>  Datetime todate in format "YYYY-MM-DD" or "YYYY-MM-DD HH:mm            
            --output-format     json,html
                                Output in format json,html
    """    
    # Get the input arguments
    args = sys.argv
    # Parse the arguments. If used an non valid argument it cause a ValueError
    options = Options()
    options.parse(args[1:])
    dict_args = vars(options.known)
    if dict_args["stats"] == True:
        # Create a stackstats object
        stats = stackstats(dict_args)
        answer_data = stats.get_answer_data()
        # Answer_ids that you fetch Stackoverflow API to get the comments
        ids = [item['answer_id'] for item in answer_data]
        comment_data = stats.get_comment_on_answer_data(ids)
        stats.calc_stats(answer_data, comment_data)
    else:
        print("Not a method in arguments")

if __name__ == '__main__':
    main()
