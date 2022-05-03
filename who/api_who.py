# sanofi_scripts/utils.py
import argparse
from utils import set_log_level, get_logger
from fct_who import *
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Init logger
func_name = "main"  # sys.argv[0]
logger = get_logger(func_name)


def main():
    # Example of execution : python api_who.py --country Mexico --StartYear 2018 --StartWeek 1 --EndYear 2022 --EndWeek 53
    # Set up the arguments of the function
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter", required=False, default="Country, area or territory")
    parser.add_argument("--country", required=True)
    parser.add_argument("--StartYear", required=True)
    parser.add_argument("--StartWeek", required=True)
    parser.add_argument("--EndYear", required=True)
    parser.add_argument("--EndWeek", required=True)
    parser.add_argument("--AgeGroup", required=False, default="Total of all age groups")
    parser.add_argument("--verbose", help="Debug mode", required=False, default=False)

    args = parser.parse_args()

    if args.verbose:
        set_log_level(logger, "debug")
        logger.debug(f"Command line arguments: {args}")

    # Report 2
    # Create a list of dictionnaries with the data from the website
    list_of_dict = parse_table2(get_table_data2())
    logger.info("List of dicts created")
    # Convert the list of dictionnaries into a dataframe
    df = pd.DataFrame.from_dict(list_of_dict)
    # Write the dataframe in a csv at the same directory as the code
    df.to_csv(
        "/mnt/c/Users/madville/Documents/who_file_report2.csv", index=False, sep="|"
    )
    logger.info("CSV writen")

    # Report 12
    # Create a list of dictionnaries with the data from the website
    list_of_dict = parse_table(
        get_table_data(
            args.country, args.StartYear, args.StartWeek, args.EndYear, args.EndWeek
        )
    )
    logger.info("List of dicts created")
    # Convert the list of dictionnaries into a dataframe
    df = pd.DataFrame.from_dict(list_of_dict)
    # Write the dataframe in a csv at the same directory as the code
    df.to_csv(
        "/mnt/c/Users/madville/Documents/who_file_report12_" + args.country + ".csv",
        index=False,
        sep="|",
    )
    logger.info("CSV writen")

    # Report 16

    # selecting options
    option_selector("ctl_ReportViewer_ctl04_ctl03_ddValue", args.filter)  # "Filter by"
    option_selector_2(
        "ctl_ReportViewer_ctl04_ctl05_ddDropDownButton",
        "ctl_ReportViewer_ctl04_ctl05_divDropDown",
        args.country,
    )  # "Select by"
    option_selector("ctl_ReportViewer_ctl04_ctl07_ddValue", args.StartYear)  # "From year"
    option_selector("ctl_ReportViewer_ctl04_ctl09_ddValue", args.EndYear)  # "To year"
    option_selector("ctl_ReportViewer_ctl04_ctl11_ddValue", args.StartWeek)  # "From week"
    option_selector("ctl_ReportViewer_ctl04_ctl13_ddValue", args.EndWeek)  # "To week"
    option_selector("ctl_ReportViewer_ctl04_ctl15_ddValue", args.AgeGroup)  # "Age group type"

    # clicking "View report"
    driver.find_element_by_id("ctl_ReportViewer_ctl04_ctl00").click()

    logger.info("Selection done")

    try:
        # waiting for data to appear
        WebDriverWait(driver, TIME_TABLE).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@id='VisibleReportContentctl_ReportViewer_ctl09']//div")
            )
        )

        # getting data
        table_rows_html = get_table_rows(
            "//div[@id='VisibleReportContentctl_ReportViewer_ctl09']//div//table//tbody//tr//td//"
            + "table//tbody//tr//td//table//tbody//tr//td//table//tbody//tr//td//table//tbody//tr"
        )
        data = get_table_content(table_rows_html)
    finally:
        # quitting selenium
        driver.quit()

    # Converting data format to dict containing columns of the future dataframe
    # (orient = 'tight' to orient = 'columns' refering to the pandas documentation briefly)
    dict = {}
    logger.debug(data["headers"])
    logger.debug(len(data["headers"][1]))
    logger.debug(data["rows"][0])
    logger.debug(len(data["rows"][0]))
    # The columns of the dataframe will have for name the concatenation of the multiple header
    # We increment the counter when the selector moves to the next highest header (called overheader)
    count_overheader = 0
    # Read data vertically to stock it in dictionnaries that will be our future columns of dataframe
    for i in range(len(data["headers"][1])):
        temp = []
        for j in range(len(data["rows"])):
            temp.append(data["rows"][j][i])
        logger.debug("Length of temp :")
        logger.debug(len(temp))
        # Increment the overheader each time we meet a column named 'Cases'
        if data["headers"][1][i] == "Cases" or data["headers"][1][i] == "Geospread":
            count_overheader += 1
        dict[data["headers"][0][count_overheader] + " " + data["headers"][1][i]] = temp
    # Debugger that read the dictionnary just created
    for key in dict:
        logger.debug(key)
        logger.debug(len(dict[key]))
    # Replacement of the Null values to real Null values and write the csv
    df = pd.DataFrame.from_dict(dict).replace("\xa0", "")
    df.to_csv(
        "/mnt/c/Users/madville/Documents/who_file_report16_" + args.country + ".csv",
        index=False,
        sep="|",
    )
    logger.info("CSV writen")

    # Report 26 (in test)
    # # Create a list of dictionnaries with the data from the website
    # list_of_dict = parse_table26(get_table_data26(args.country, args.StartYear, args.StartWeek, args.EndYear, args.EndWeek))
    # logger.info('List of dicts created')
    # # Convert the list of dictionnaries into a dataframe
    # df = pd.DataFrame.from_dict(list_of_dict)
    # # Write the dataframe in a csv at the same directory as the code
    # df.to_csv('who_file_report26.csv',index=False,sep='|')
    # logger.info('CSV writen')


if __name__ == "__main__":
    set_log_level(logger, "info")
    main()
