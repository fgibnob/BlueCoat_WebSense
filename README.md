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
- [ ] add handling for URLs without a category but rated by the WebPulse system.
- [ ] add handling for URLs that are not categorised.
- [ ] add command line option for single URL queries.
- [ ] add option to save output to json file.
- [ ] fix handling of filename input ie, parser.add_argument('file', type=argparse.FileType('r'))
        https://docs.python.org/2/library/argparse.html#type
        currently the filename argument accepts any string
- [ ] create handler for internal ip ranges.
- [ ] add option to sanitize URL by adding '[' and ']' either side of the : in URL.
