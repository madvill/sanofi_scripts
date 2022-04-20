import urllib.parse

import requests
from bs4 import BeautifulSoup


#####
# We define 2 header blocks that will be used for the 2 POST requests in `get_table_data`. These headers come from a
# fresh access of the website using Firefox 95's developer tools.
#####

post_headers_display_report = """Host: apps.who.int
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Origin: https://apps.who.int
DNT: 1
Connection: keep-alive
Referer: https://apps.who.int/flumart/Default?ReportNo=12
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1"""

post_headers_table_data = """Host: apps.who.int
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
X-Requested-With: XMLHttpRequest
X-MicrosoftAjax: Delta=true
Cache-Control: no-cache
Content-Type: application/x-www-form-urlencoded; charset=utf-8
Origin: https://apps.who.int
DNT: 1
Connection: keep-alive
Referer: https://apps.who.int/flumart/Default?ReportNo=12
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
TE: trailers"""

#####
# End of our header blocks.
#####


def parse_headers(headers):
    """
        Turn the single multi-line string of headers into a dict that requests can use.
    """
    return dict(line.split(': ') for line in filter(None, headers.split('\n')))


def get_important_hidden_input_values(html):
    """
        Grab and return the 3 important input values from the HTML response:
            * __VIEWSTATE
            * __VIEWSTATEGENERATOR
            * __EVENTVALIDATION
    """
    soup = BeautifulSoup(html, 'lxml')

    viewstate = soup.find_all('input', {'id': '__VIEWSTATE'})
    assert len(viewstate) == 1
    viewstate = viewstate[0]['value']

    viewstategenerator = soup.find_all('input', {'id': '__VIEWSTATEGENERATOR'})
    assert len(viewstategenerator) == 1
    viewstategenerator = viewstategenerator[0]['value']

    eventvalidation = soup.find_all('input', {'id': '__EVENTVALIDATION'})
    assert len(eventvalidation) == 1
    eventvalidation = eventvalidation[0]['value']

    return (viewstate, viewstategenerator, eventvalidation)


def get_table_data(country, from_year, from_week, to_year, to_week):
    """
        Issue 3 HTTP requests to get the tabular data we want:
            1. First, issue a GET request to the root page. This will 1) set the cookies and 2) allow us to grab the
               3 important input values (see `get_important_hidden_input_values`) so that we can issue the next POST
               request.
            2. Second, issue a POST request that will return a new table skeleton. This POST request will yield 3
               *new* important input values that must be used for the next and final POST request.
            3. Finally, issue a POST request that will grab the actual data to populate the skeleton table.
        This chaining of requests is important. Without the first request, we won't have the cookies and 3 important
        input values to issue the second request. Without the second request, we won't have the 3 *new* important
        input values to issue the third request. VERY TRICKY!
    """
    with requests.Session() as s:
        # Issue the first request (GET) to set the Session's cookies and grab the first batch of 3 important input
        # values.
        response = s.get('https://apps.who.int/flumart/Default?ReportNo=12')
        viewstate, viewstategenerator, eventvalidation = get_important_hidden_input_values(response.text)

        # Construct the POST payload needed for the second request.
        data = data_format_display_report(viewstate,
                                          viewstategenerator,
                                          eventvalidation,
                                          country,
                                          from_year,
                                          from_week,
                                          to_year,
                                          to_week)

        # Issue the second request (POST) to grab the table skeleton and 3 *new* important input values.
        response = s.post('https://apps.who.int/flumart/Default?ReportNo=12',
                          data=data,
                          headers=parse_headers(post_headers_display_report))
        viewstate, viewstategenerator, eventvalidation = get_important_hidden_input_values(response.text)

        # Construct the POST payload needed for the third request.
        data = data_format_table_data(viewstate,
                                      viewstategenerator,
                                      eventvalidation,
                                      country,
                                      from_year,
                                      from_week,
                                      to_year,
                                      to_week)

        # Finally, issue the last request (POST) to grab the contents for the table skeleton.
        response = s.post('https://apps.who.int/flumart/Default?ReportNo=12',
                          data=data,
                          headers=parse_headers(post_headers_table_data))

        # Return the HTML content meant to go inside the table skeleton.
        return response.text


def parse_table(html):
    """
        Parse the table contents into a more useful data structure.
        TODO: Create a Pandas DataFrame from the contents.
    """
    soup = BeautifulSoup(html, 'lxml')
    _, _, h, *body = [list(filter(None, [i.get_text(strip=True) for i in b.select('td')])) 
        for b in soup.select('table table table table tr:nth-of-type(5) table tr')]
    return [dict(zip([*filter(None, h)], i)) for i in body]


def data_format_display_report(viewstate, viewstategenerator, eventvalidation, country, from_year, from_week, to_year, to_week):
    """
        Construct the POST payload for the second request in `get_table_data` that gets the table skeleton.
    """
    return f'__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE={urllib.parse.quote(viewstate)}&__VIEWSTATEGENERATOR={urllib.parse.quote(viewstategenerator)}&__EVENTVALIDATION={urllib.parse.quote(eventvalidation)}&ddlFilterBy=1&lstSearchBy={country}&ctl_list_YearFrom={from_year}&ctl_list_WeekFrom={from_week}&ctl_list_YearTo={to_year}&ctl_list_WeekTo={to_week}&ctl_ViewReport=Display+report'


def data_format_table_data(viewstate, viewstategenerator, eventvalidation, country, from_year, from_week, to_year, to_week):
    """
        Construct the POST payload for the third request in `get_table_data` that gets the actual table contents.
    """
    return f'ScriptManager1=ScriptManager1%7Cctl_ReportViewer%24ctl09%24Reserved_AsyncLoadTarget&__EVENTTARGET=ctl_ReportViewer%24ctl09%24Reserved_AsyncLoadTarget&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE={urllib.parse.quote(viewstate)}&__VIEWSTATEGENERATOR={urllib.parse.quote(viewstategenerator)}&__EVENTVALIDATION={urllib.parse.quote(eventvalidation)}&ddlFilterBy=1&lstSearchBy={country}&ctl_list_YearFrom={from_year}&ctl_list_WeekFrom={from_week}&ctl_list_YearTo={to_year}&ctl_list_WeekTo={to_week}&ctl_ReportViewer%24ctl03%24ctl00=&ctl_ReportViewer%24ctl03%24ctl01=&ctl_ReportViewer%24ctl10=ltr&ctl_ReportViewer%24ctl11=standards&ctl_ReportViewer%24AsyncWait%24HiddenCancelField=False&ctl_ReportViewer%24ctl04%24ctl03%24ddValue=1&ctl_ReportViewer%24ctl04%24ctl05%24ddValue=1&ctl_ReportViewer%24ToggleParam%24store=&ctl_ReportViewer%24ToggleParam%24collapse=false&ctl_ReportViewer%24ctl05%24ctl00%24CurrentPage=&ctl_ReportViewer%24ctl05%24ctl03%24ctl00=&ctl_ReportViewer%24ctl08%24ClientClickedId=&ctl_ReportViewer%24ctl07%24store=&ctl_ReportViewer%24ctl07%24collapse=false&ctl_ReportViewer%24ctl09%24VisibilityState%24ctl00=None&ctl_ReportViewer%24ctl09%24ScrollPosition=&ctl_ReportViewer%24ctl09%24ReportControl%24ctl02=&ctl_ReportViewer%24ctl09%24ReportControl%24ctl03=&ctl_ReportViewer%24ctl09%24ReportControl%24ctl04=100&__ASYNCPOST=true&'


print(parse_table(get_table_data('Brazil', '2020', '1', '2021', '53')))