import argparse
from utils import set_log_level, get_logger
from os import listdir
from os.path import isfile, join

from fct_unpivot import unpivot_file

# Init logger
func_name = 'main' # sys.argv[0]
logger = get_logger(func_name)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", help="Input file path", required=True)
    # parser.add_argument("--country", required=False)
    parser.add_argument("--verbose", help="Debug mode", required=False, default=False)

    args = parser.parse_args()

    if args.verbose:
        set_log_level(logger, "debug")
        logger.debug(f"Command line arguments: {args}")
    # Apply the unpivot function to all the files of the directory that aren't already pivoted files
    if args.dir[-1] == "/" :
        all_files = [
            f for f in listdir(args.dir) if isfile(join(args.dir, f)) and "pivoted" not in f
        ]
        for file in all_files:
            logger.info("Start unpivot function for " + file)
            unpivot_file(args.dir + file, args.dir.split("/")[-2])
            logger.info("Melting successful")
    # Apply the unpivot function to one file with method of the correspond country
    else :
        all_files = [args.dir]
        logger.info("Start unpivot function for " + args.dir.split("/")[-1])
        unpivot_file(args.dir, args.dir.split("/")[-2])
        logger.info("Melting successful")



if __name__ == "__main__":
    set_log_level(logger, "info")
    main()
