import argparse
import ast
from getInflation import get_inflation_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieves inflation index data (ICP) from primary source ECB and plots year-on-year inflation rate.')
    parser.add_argument('-b', '--begin', type=str, help='Start date in YYYY-MM format', default=None)
    parser.add_argument('-e', '--end', type=str, help='End date in YYYY-MM format', default=None)
    parser.add_argument('-s', '--save-output', type=str, help='Saves the created image (.png) and interactive HTML to output folder (Default is false).', default='False')
    args = parser.parse_args()
    
    save_output = ast.literal_eval(args.save_output)

    get_inflation_data(args.begin, args.end, save_output)