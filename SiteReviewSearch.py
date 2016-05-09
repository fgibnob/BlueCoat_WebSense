#!/usr/bin/env python
 
__description__  = 'Program to query Blue Coat SiteReview for a URLs category'
__requirements__ = 'Beautiful Soup 4 Library ; http://www.crummy.com/software/BeautifulSoup/#Download' \
                   'Requests Library         ; https://pypi.python.org/pypi/requests'
__author__       = 'SL'
__email__        = ''
__version__      = '0.1.0'
__date__         = '25/11/2014'
 
 
"""
Source code is provided as is and without warranty or support
Use at your own risk

History:
    23/10/2014: 0.0.1 start
    23/10/2014: 0.0.2 added BeautifulSoup function to strip HTML tabs from JSON response
    24/10/2014: 0.0.3 added function to retrieve the URLs reviewed date
    03/11/2014: 0.0.4 added output csv (Thanks to Didier Stevens for letting me use his LogToCSV class and
                      Timestamp function)
    18/11/2014: 0.0.5 added argparse support for a input files
    18/11/2014: 0.0.5 added restriction on number of requests per minute
    25/11/2014  0.0.6 reformatted terminal output
    16/11/2015  0.0.7 added support for threat risk level

Todo:
    add handling for URLs without a category but rated by the WebPulse system
    add handling for URLs that are not rated
    add command line options single URL queries
    add output to json file
    fix handling of filename input ie, parser.add_argument('file', type=argparse.FileType('r'))
        https://docs.python.org/2/library/argparse.html#type
        currently the filename argument accepts any string
    add option to submit url as an argument
    add handler for internal ip ranges
    add option to sanitize URL by adding '[' and ']' either side of the : in URL

Bugs:
    24/10/2014: BUG001 Web sites that are rated with the WebPulse system and do not return a Last Time/Reviewed date
    return an incomplete value when parsed by the GetReturnReviewed function
"""
 
import time
import json
import requests
import argparse
from bs4 import BeautifulSoup
 
 
WEBPULSE_SITEREVIEW_URL = 'http://sitereview.bluecoat.com/rest/categorization'
 
 
def Timestamp(epoch=None):
# get current timestamp
 
    if epoch == None:
        localTime = time.localtime()
    else:
        localTime = time.localtime(epoch)
    return '%04d%02d%02d-%02d%02d%02d' % localTime[0:6]
 
 
class LogToCSV():
 
    def __init__(self, prefix, headers, separator='\t'):
    # create CSV file to write to
        self.separator = separator
        self.filename = '%s-%s.csv' % (prefix, Timestamp())
        self.f = open(self.filename, 'w')
        self.f.write(self.separator.join(headers) + '\n')
        self.f.close()
 
    def PrintAndLog(self, formats, parameters):
    # write results to CSV file
 
        line = self.separator.join(formats) % parameters
        f = open(self.filename, 'a')
        f.write(line + '\n')
        f.close()
 
 
def DrinkSoup(a):
# strip HTML tags from requests content
 
    soup = BeautifulSoup(a, "html.parser")
    return soup.get_text()
 
 
def GetDateReviewed(findsubmitdate):
# extract the category review date.
 
    try:
        reviewdate = findsubmitdate[0:findsubmitdate.find('\xa0')]
        return reviewdate
    except AttributeError:
        return
 
 
def SiteReviewSearch(filename, options):
 
    global oLogger
 
    headers = ('URL', 'Categorisation', 'Unrated?', 'Review_Date')
    oLogger = LogToCSV('sitereview-search', headers)

    print('[Querying Blue Coat SiteReview]')

    with open(filename, 'r') as f:
        for line in f:
            payload = {'url': line}
            headers = {'Referer': 'http://www.sitereview.bluecoat.com/sitereview.jsp'}
            r = requests.post(WEBPULSE_SITEREVIEW_URL, data=payload, headers=headers)
 
            data = DrinkSoup(r.content)
 
            json_response = json.loads(data)
            last_review = (GetDateReviewed(json_response['ratedate']))
            formats = ('%s', '%s', '%s', '%s', '%s')
            parameters = (json_response['url'], json_response['categorization'], json_response['unrated'], json_response['threatrisklevel'], last_review)
            print('url               :', json_response['url'])
            print('categorization    :', json_response['categorization'])
            print('unrated           :', json_response['unrated'])
            print('threat risk level :', json_response['threatrisklevel'])
            if json_response['unrated'] == True:
                print('last review:   : Not reviewed')
            else:
                print('last review:   :', last_review)
            print('')
            oLogger.PrintAndLog(formats, parameters)
            time.sleep(options.delay)
 
 
def Main():
 
    parser = argparse.ArgumentParser(usage='%(prog)s [options] filename\n', description=__description__)
    parser.add_argument('filename')
    parser.add_argument('-d', '--delay', type=int, default=5, help='delay in seconds between queries')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    args = parser.parse_args()
 
    SiteReviewSearch(args.filename, args)
 
if __name__ == '__main__':
    Main()
