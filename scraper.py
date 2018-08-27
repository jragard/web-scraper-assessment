"""
Simple Web Scraper

A command line program to scrape a single web page, extracting any URLs, email
addresses, and phone numbers it contains.

"""

import argparse
import requests
import re
import sys
from HTMLParser import HTMLParser


class MyHTMLParser(HTMLParser):
    url_list = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.url_list.append(attrs[0][1])
        elif tag == 'img':
            self.url_list.append(attrs[0][1])

    def handle_data(self, data):
        print 'Encountered Data', data


def scrape_url(url):
    """ Takes a url from command line arg and retrieves the text of the
    webpage, parsing out any URLs, email addresses, or phone numbers included
    in the HTML
    """
    r = requests.get(url)
    url_list = []
    email_list = []
    phone_list = []

    # URL regex
    http_match = re.findall(r'https:\/\/[\w\/?=.-]+', r.text)
    if http_match:
        for match in http_match:
            if match not in url_list:
                url_list.append(match)

    # HTML Parser
    parser = MyHTMLParser()
    parser.feed(r.text)
    merged_list = url_list + parser.url_list
    output = set(merged_list)

    # Email regex
    email_match = re.findall(r'[\w.-]+@[\w.-]+.\w+', r.text)
    if email_match:
        for match in email_match:
            if match not in email_list:
                email_list.append(match)

    email_list = set(email_list)

    # Phone number regex
    phone_match = re.findall(r'\d\d\d-\d\d\d-\d\d\d\d', r.text)
    if phone_match:
        for match in phone_match:
            if match not in phone_list:
                phone_list.append(match)

    phone_list = set(phone_list)

    print ''
    print ''

    if len(url_list) != 0:
        print 'URLS Found'
        print '**************************************************'
        print ''
        print ''
        for url in output:
            print url
        print ''
        print ''
    else:
        print 'URLs Found'
        print '**************************************************'
        print ''
        print ''
        print 'None'
        print ''
        print ''

    if len(email_list) != 0:
        print 'Emails Found'
        print '**************************************************'
        print ''
        print ''
        for email in email_list:
            print email
        print ''
        print ''
    else:
        print 'Emails Found'
        print '**************************************************'
        print ''
        print ''
        print 'None'
        print ''
        print ''

    if len(phone_list) != 0:
        print 'Phone Numbers Found'
        print '**************************************************'
        print ''
        print ''
        for number in phone_list:
            print number
        print ''
        print ''
    else:
        print 'Phone Numbers Found'
        print '**************************************************'
        print ''
        print ''
        print 'None'
        print ''
        print ''


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='url to scrape')
    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    # parser.feed(args)

    parsed_args = parser.parse_args(args)
    # parser.feed(par)
    scrape_url(parsed_args.url)


if __name__ == '__main__':
    main(sys.argv[1:])
