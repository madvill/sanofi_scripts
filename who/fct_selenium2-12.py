from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import Select

########################## Code for ReportNo2 ############################### IT WORKS

# # PATH to chromedrive.exe
# PATH = "/mnt/c/Users/madville/Downloads/chromedriver_win32/chromedriver.exe"
# driver = webdriver.Chrome(PATH)
# REPORT2_URL = "https://apps.who.int/flumart/Default?ReportNo=2"
# driver.get(REPORT2_URL)
# TIME_TABLE = 900

# # func to get all rows from data table
# def get_table_rows(xpath):
#     # finding all rows from table by xpath
#     table_rows = driver.find_elements(By.XPATH, xpath)
#     table_html = []
#     # appending html for each row into a list 
#     for row in table_rows:
#         table_html.append(row.get_attribute('innerHTML'))
#     return table_html

# # func to parse rows into a dictionary
# def get_table_content(table_rows_html):
#     # data dictionary with headers and rows
#     data = {
#         'headers': [],
#         'rows': [],
#     }
#     # looping through each row, and parsing it's html
#     for i in range(len(table_rows_html)):
#         # setting up beautiful soup
#         soup = BeautifulSoup(table_rows_html[i], 'html.parser')
#         # differentiating logic for rows and headers:
#         # if the html content has at least one span tag, it's considered a row
#         # if the html content has more than one div tag and no span tag, it's considered a header
#         # getting all spans and div tags (for testing rows and headers), and all tds
#         td_html = soup.find_all("td", recursive=False)
#         span_html = soup.find_all("span")
#         div_html = soup.find_all("div")
#         # data to append to dictionary
#         headers_data = []
#         rows_data = []
#         # headers
#         if len(div_html) > 1 and not span_html:
#             for header in td_html:
#                 headers_data.append(header.get_text())
#             data['headers'].append(headers_data)
#         # rows
#         elif len(div_html) > 1 and span_html:
#             for row in td_html:
#                 if not row.get_text() == '':
#                     rows_data.append(row.get_text())
#             data['rows'].append(rows_data)
#     return data

# try:
#     # waiting for data to appear
#     WebDriverWait(driver, TIME_TABLE).until(EC.presence_of_element_located((By.XPATH, "//div[@id='VisibleReportContentctl_ReportViewer_ctl09']//div")))

#     # getting data
#     # It's actually not the good pattern of html bracket for the report no2
#     # I adapted the transformation in dictionnary below instead of touching this pattern
#     # The right thing would be to modify this pattern and get the initial transformation code 
#     table_rows_html = get_table_rows("//div[@id='VisibleReportContentctl_ReportViewer_ctl09']//div//table//tbody//tr//td//" + 
#                                             "table//tbody//tr//td//table//tbody//tr//td//table//tbody//tr//td//table//tbody//tr")
#     data = get_table_content(table_rows_html)
# finally:
#     # quitting selenium
#     driver.quit()

# dict = {}

# # The columns of the dataframe will have for name the concatenation of the multiple header
# # We increment the counter when the selector moves to the next highest header (called overheader)

# # Code adapted because i don't want to touch the html pattern above
# # Read data vertically to stock it in dictionnaries that will be our future columns of dataframe
# for i in range(len(data["headers"][1])):
#     temp = []
#     for j in range(len(data["headers"])-2):
#         temp.append(data["headers"][j+2][i])

#     dict[data["headers"][1][i]] = temp
# # Debugger that read the dictionnary just created

# # Replacement of the Null values to real Null values and write the csv
# df = pd.DataFrame.from_dict(dict).replace("\xa0", "")
# del df[""]
# df.to_csv('who_file_report_selenium2.csv',index=False,sep='|')


########################## Code for ReportNo2 ###############################

# PATH to chromedrive.exe
PATH = "/mnt/c/Users/madville/Downloads/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(PATH)
REPORT12_URL = "https://apps.who.int/flumart/Default?ReportNo=12"
driver.get(REPORT12_URL)
TIME_TABLE = 900
TIME_OPTIONS = 30

# func to get all rows from data table
def get_table_rows(xpath):
    # finding all rows from table by xpath
    table_rows = driver.find_elements(By.XPATH, xpath)
    table_html = []
    # appending html for each row into a list 
    for row in table_rows:
        table_html.append(row.get_attribute('innerHTML'))
    return table_html

# func to get all rows from data table
def get_table_rows(xpath):
    # finding all rows from table by xpath
    table_rows = driver.find_elements(By.XPATH, xpath)
    table_html = []
    # appending html for each row into a list 
    for row in table_rows:
        table_html.append(row.get_attribute('innerHTML'))
    return table_html

# func to parse rows into a dictionary
def get_table_content(table_rows_html):
    # data dictionary with headers and rows
    data = {
        'headers': [],
        'rows': [],
    }
    # looping through each row, and parsing it's html
    for i in range(len(table_rows_html)):
        # setting up beautiful soup
        soup = BeautifulSoup(table_rows_html[i], 'html.parser')
        # differentiating logic for rows and headers:
        # if the html content has at least one span tag, it's considered a row
        # if the html content has more than one div tag and no span tag, it's considered a header
        # getting all spans and div tags (for testing rows and headers), and all tds
        td_html = soup.find_all("td", recursive=False)
        span_html = soup.find_all("span")
        div_html = soup.find_all("div")
        # data to append to dictionary
        headers_data = []
        rows_data = []
        # headers
        if len(div_html) > 1 and not span_html:
            for header in td_html:
                if not row.get_text() == '':
                    headers_data.append(header.get_text())
            data['headers'].append(headers_data)
        # rows
        elif len(div_html) > 1 and span_html:
            for row in td_html:
                if not row.get_text() == '':
                    rows_data.append(row.get_text())
            data['rows'].append(rows_data)
    return data

select_element = driver.find_element(By.ID,'ddlFilterBy')
select_object = Select(select_element)
select_object.select_by_visible_text("Country, area or territory")

select_element = driver.find_element(By.ID,'lstSearchBy')
select_object = Select(select_element)
select_object.select_by_visible_text("Mexico")

select_element = driver.find_element(By.ID,'ctl_list_YearFrom')
select_object = Select(select_element)
select_object.select_by_visible_text("2018")

select_element = driver.find_element(By.ID,'ctl_list_YearTo')
select_object = Select(select_element)
select_object.select_by_visible_text("2022")

select_element = driver.find_element(By.ID,'ctl_list_WeekFrom')
select_object = Select(select_element)
select_object.select_by_visible_text("1")

select_element = driver.find_element(By.ID,'ctl_list_WeekTo')
select_object = Select(select_element)
select_object.select_by_visible_text("53")

driver.find_element_by_name("ctl_ViewReport").click()

try:
    # waiting for data to appear
    WebDriverWait(driver, TIME_TABLE).until(EC.presence_of_element_located((By.XPATH, "//div[@id='VisibleReportContentctl_ReportViewer_ctl09']//div")))

    # getting data
    # It's actually not the good pattern of html bracket for the report no2
    # I adapted the transformation in dictionnary below instead of touching this pattern
    # The right thing would be to modify this pattern and get the initial transformation code 
    table_rows_html = get_table_rows("//div[@id='VisibleReportContentctl_ReportViewer_ctl09']//div//table//tbody//tr//td//" + 
                                            "table//tbody//tr//td//table//tbody//tr//td//table//tbody//tr//td//table//tbody//tr")
    data = get_table_content(table_rows_html)
finally:
    # quitting selenium
    driver.quit()

dict = {}
# Read data vertically to stock it in dictionnaries that will be our future columns of dataframe
data["headers"][1].remove("")
del(data["rows"][0]) # We don't want "Data from : All sites" in our table
for i in range(len(data["headers"][1])):
    temp = []
    for j in range(len(data["rows"])):
        temp.append(data["rows"][j][i])

    dict[data["headers"][1][i]] = temp

# Replacement of the Null values to real Null values and write the csv
df = pd.DataFrame.from_dict(dict).replace("\xa0", "")
df.to_csv('who_file_report_selenium12.csv',index=False,sep='|')

# Replacement of the Null values to real Null values and write the csv
df = pd.DataFrame.from_dict(dict).replace("\xa0", "")

df.to_csv('who_file_report_selenium12.csv',index=False,sep='|')



