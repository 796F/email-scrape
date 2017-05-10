import re, sys, getopt, csv
import requests

from HTMLParser import HTMLParser

class EmailParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.active = False
        self.current_email = ""

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            key, value = attr
            if 'mailto' in value:
                if tag == 'a' :
                    self.active = True
                    email = re.findall(EMAIL_REGEX, value)[0]
                    self.current_email = email

    def handle_endtag(self, tag):
        if tag == 'a':
            self.active = False
            self.current_email = ""

    def handle_data(self, data):
        if self.active:
            self.current_email += ", " + ", ".join(data.split(' '))
            print self.current_email

EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

def main(argv):
    if len(argv) == 1:
        url = argv[0]
        r = requests.get(url)
        parser = EmailParser()
        parser.feed(r.content)

if __name__ == "__main__":
    main(sys.argv[1:])
