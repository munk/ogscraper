OG Scraper
==========

### Commandline Execution:

    $ chmod +x og_scraper.py
    $ ./og_scraper.py

### REPL Execution:


    In[1]: import og_scraper as og
    In[2]: og.main()


### Dependencies
The Python standard library. It is developed against 2.7, but is also forwards compatible with 3.5.

### Testing

You can run tests with py.test or nose.

### Possible Bugs

Running `document.getElementsByTagName('*').length` in the javascript console shows 235 elements, but this program counts 229. It's possible that the difference is due to nodes being added via running javascript. It's also possible that HTMLParser and the javascript engines in Chrome and Firefox disagree about whether some elements are well formed.


Walkthrough & Critique
=======

### Headers

    #!/usr/bin/env python
    from __future__ import print_function

Using the magic of time travel, this gives us print as a function, rather than a statement. PEP-3105 discusses the rationale for this. 
 
    from collections import Counter

This is a nice tool from the standard library that provides a class to convert from a sequence of elements to a dictionary with the elements as keys and their counts as values. It's nicer than writing something like this all over the place:

    def count(items):
        counter = {}
        for i in items:
            counter[i] = counter.get(i, 0) + 1
        return counter

    try:
        from urllib import urlopen
        from HTMLParser import HTMLParser
    except ImportError:
        from html.parser import HTMLParser
        from urllib.request import urlopen

This does conditional imports based on whether we're using python 2 or 3. Writing forwards compatible code now can help keep maintenance costs down later.

### HTTP Requests

    def fetch_html(url):
        f = urlopen(url)
        return str(f.read())

The python docs recommend `requests` over using urllib because of the better api, but if we're avoiding external dependencies, this is the way to go. `urllib` treats the page as a sort of file object with a `read()` method. Unfortunately, it does not have a context manager, so you can't use the nice `with` syntax. 

### The Parser

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

This class is the heart of this program. It extends HTMLParser from the standard library. In python2, this is an old style class, so we're forced to use the `<Class>.__init__` syntax over `super().__init()`.

The overriden `handle_starttag` is called when parser.feed(string) is executed. During parsing, whenever a start tag is found, it adds the tag name to this class' local state. In other applications, it might be used to update the syntax tree in a DOM, for example. 

I also provide two addtional methods, `total_tag_count` and `top_tags`. The former method does what it says and returns the length of the tag list. The uses Counter to count the tags, converts them to a sorted list of tuples and returns the k most frequent elements.

It would have been possible to write a function to parse the html, perhaps using a regular expression. Something like `<[A-Za-z]+` probably would have sufficed, but I decided against it for a few reasons.

The first is of course 'Some people, when confronted with a problem, think "I know, I'll use regular expressions." Now they have two problems.'. Regular expressions suffer from readability and testability problems, so they're not very maintanable. The second is that if this parser were to grow, regexs would be a liability, as html is a context free language, not a regular language. Finally, reusing tested, well used code in a standard library is always preferable to a buggy first pass.


    def main():
        url = "http://ordergroove.com/company"
        html = fetch_html(url)
        parser = OGParser()
        parser.feed(html)
        tag_count = parser.total_tag_count()
        top_five_tags = parser.top_tags(5)
        print("There are {} tags".format(tag_count))
        print("The top 5 tags are {}".format(top_five_tags))
    
    if __name__ == '__main__':
        main()

This is the actual orchestration of the program. It's hidden behind a function to make this file reusable.


