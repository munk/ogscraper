from __future__ import print_function
from collections import Counter

try:
    from urllib import urlopen
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser
    from urllib.request import urlopen

def fetch_html(url):
    f = urlopen(url)
    return str(f.read())

class OGParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)

    def total_tag_count(self):
        return len(self.tags)

    def top_tags(self, ct):
        counted_tags = Counter(self.tags)
        tags = sorted(counted_tags.items(), key=lambda tag: tag[1], reverse=True)
        return tags[0:ct]


def main():
    url = "http://ordergroove.com/company"
    html = fetch_html(url)
    parser = OGParser()
    parser.feed(html)
    tag_count = parser.total_tag_count()
    top_five_tags = parser.top_tags(5)
    print("There are %s tags" % tag_count)
    print("The top 5 tags are %s" % top_five_tags)

if __name__ == '__main__':
    main()
