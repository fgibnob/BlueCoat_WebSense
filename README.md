# BlueCoat_WebSense

### Description
A python program to query Blue Coat SiteReview for a URL's category.

### Usage
usage: SiteReviewSearch.py [options] filename

Program to query Blue Coat SiteReview for a URLs category

positional arguments:
  filename

optional arguments:
  -h, --help            show this help message and exit
  -d DELAY, --delay DELAY
                        delay in seconds between queries
  --version             show program's version number and exit

### Requirements
- Beautiful Soup 4 Library ; http://www.crummy.com/software/BeautifulSoup/#Download
- Requests Library         ; https://pypi.python.org/pypi/requests
- Python 3

### Todo
- [ ] accept url or ip as positional argument.
- [ ] add support for local pickle database.
- [ ] add function to leverage K9 API to allow unlimited lookups.
