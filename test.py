from pickle import FALSE
import sys
import argparse
from utils import set_log_level, get_logger

# Init logger
logger = get_logger('ma fonction trop cool')


def main():
    parser = argparse.ArgumentParser(description='lol')
    parser.add_argument('--filename', help="Input file path", required=True)
    parser.add_argument('--verbose', help="Debug mode", required=False, default=False)


    args = parser.parse_args()

    logger.info(args.filename)


    if args.verbose:
        set_log_level(logger,"debug")
        logger.debug(f"Command line arguments: {args}")

if __name__ == "__main__":
    set_log_level(logger,"info") 
    main()

