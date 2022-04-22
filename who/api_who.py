# sanofi_scripts/utils.py
import argparse
import csv
from utils import set_log_level, get_logger
from fct_who import *
import pandas as pd

# Init logger
func_name = 'main' # sys.argv[0]
logger = get_logger(func_name)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--country", required=False)
    parser.add_argument("--StartYear", required=False)
    parser.add_argument("--StartWeek", required=False)
    parser.add_argument("--EndYear", required=False)
    parser.add_argument("--EndWeek", required=False)
    parser.add_argument("--verbose", help="Debug mode", required=False, default=False)

    args = parser.parse_args()

    if args.verbose:
        set_log_level(logger, "debug")
        logger.debug(f"Command line arguments: {args}")

    # Report 2 (IT WORKS)
    # list_of_dict = parse_table2(get_table_data2()) 
    # logger.info('List of dicts created')
    # df = pd.DataFrame.from_dict(list_of_dict)
    # df.to_csv('who_file_report12.csv',index=False,sep='|')
    # logger.info('CSV writen')


    # Report 12 (IT WORKS)
    # list_of_dict = parse_table(get_table_data(args.country, args.StartYear, args.StartWeek, args.EndYear, args.EndWeek))
    # logger.info('List of dicts created')
    # df = pd.DataFrame.from_dict(list_of_dict)
    # df.to_csv('who_file_report12.csv',index=False,sep='|')
    # logger.info('CSV writen')

    # Report 16 (need request) (Country/area or territory is not a normal drop down panel and we can't write inside the box, the informations are external to the website)
    # soup = parse_table16(get_table_data16('France', '2020', '1', '2021', '53'))
    # logger.info(soup)
    # logger.info('List of dicts created')
    # df16 = pd.DataFrame.from_dict(list_of_dict16)
    # df16.to_csv('who_file_report16.csv',index=False,sep='|')
    # logger.info('CSV writen')

    # Report 26 (can't open) (format seems to be the same as 16)

if __name__ == "__main__":
    set_log_level(logger, "info")
    main()