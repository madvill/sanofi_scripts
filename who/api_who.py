# sanofi_scripts/utils.py
import argparse
import csv
from ..utils import set_log_level, get_logger
from fct_who import *
import csv
# Init logger
func_name = 'main' # sys.argv[0]
logger = get_logger(func_name)

def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--reports", help="ReportNo wanted", required=True)
    # parser.add_argument("--country", required=False)
    # parser.add_argument("--region", required=False)
    parser.add_argument("--verbose", help="Debug mode", required=False, default=False)

    args = parser.parse_args()

    if args.verbose:
        set_log_level(logger, "debug")
        logger.debug(f"Command line arguments: {args}")


    list_of_dict = parse_table(get_table_data('Brazil', '2020', '1', '2021', '53'))
    keys = list_of_dict[0].keys()

    with open('who_file.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dict)


if __name__ == "__main__":
    set_log_level(logger, "info")
    main()