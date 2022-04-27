# sanofi_scripts/utils.py
import argparse
from utils import set_log_level, get_logger
from fct_who import *
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

# Init logger
func_name = 'main' # sys.argv[0]
logger = get_logger(func_name)

def main():
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

    # Report 2 (IT WORKS)
    list_of_dict = parse_table2(get_table_data2()) 
    logger.info('List of dicts created')
    df = pd.DataFrame.from_dict(list_of_dict)
    df.to_csv('who_file_report2.csv',index=False,sep='|')
    logger.info('CSV writen')


    # Report 12 (IT WORKS)
    list_of_dict = parse_table(get_table_data(args.country, args.StartYear, args.StartWeek, args.EndYear, args.EndWeek))
    logger.info('List of dicts created')
    df = pd.DataFrame.from_dict(list_of_dict)
    df.to_csv('who_file_report12.csv',index=False,sep='|')
    logger.info('CSV writen')

    # Report 16 

    # selecting options
    # option_selector("ctl_ReportViewer_ctl04_ctl03_ddValue", args.filter) # "Filter by"
    # option_selector_2("ctl_ReportViewer_ctl04_ctl05_ddDropDownButton", "ctl_ReportViewer_ctl04_ctl05_divDropDown", args.country) # "Select by"
    # option_selector("ctl_ReportViewer_ctl04_ctl07_ddValue", args.StartYear) # "From year"
    # option_selector("ctl_ReportViewer_ctl04_ctl09_ddValue", args.EndYear) # "To year"
    # option_selector("ctl_ReportViewer_ctl04_ctl11_ddValue", args.StartWeek) # "From week"
    # option_selector("ctl_ReportViewer_ctl04_ctl13_ddValue", args.EndWeek) # "To week"
    # option_selector("ctl_ReportViewer_ctl04_ctl15_ddValue", args.AgeGroup) # "Age group type"

    # # clicking "View report"
    # element_click("ctl_ReportViewer_ctl04_ctl00")

    # logger.info("Selection done")
    
    # try:
    #     # waiting for data to appear
    #     WebDriverWait(driver, TIME_TABLE).until(EC.presence_of_element_located((By.XPATH, "//div[@id='VisibleReportContentctl_ReportViewer_ctl09']//div")))

    #     # getting data
    #     table_rows_html = get_table_rows("//div[@id='VisibleReportContentctl_ReportViewer_ctl09']//div//table//tbody//tr//td//" + 
    #                                             "table//tbody//tr//td//table//tbody//tr//td//table//tbody//tr//td//table//tbody//tr")
    #     data = get_table_content(table_rows_html)
    # finally:
    #     # quitting selenium
    #     driver.quit()
    
    # # Converting data format to dict containing columns of the future dataframe
    # dict = {}
    # logger.info(data["headers"])
    # logger.info(len(data["headers"][1]))
    # logger.info(data["rows"][0])
    # logger.info(len(data["rows"][0]))
    # cpt_overheader = 0
    # for i in range(len(data["headers"][1])):
    #     temp = []
    #     for j in range(len(data["rows"])):
    #         temp.append(data["rows"][j][i])
    #     logger.debug("Length of temp :")
    #     logger.debug(len(temp))
        
    #     if data["headers"][1][i] == 'Cases' or data["headers"][1][i] == 'Geospread':
    #         cpt_overheader+=1
    #     dict[data["headers"][0][cpt_overheader] +" "+ data["headers"][1][i]] = temp
    
    # for key in dict :
    #     logger.debug(key)
    #     logger.debug(len(dict[key]))
    # df = pd.DataFrame.from_dict(dict).replace("\xa0", "")
    # df.to_csv('who_file_report16.csv',index=False,sep='|')
    # logger.info('CSV writen')

if __name__ == "__main__":
    set_log_level(logger, "info")
    main()