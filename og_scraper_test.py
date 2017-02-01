import og_scraper

def test_total_tag_count():
    html = "<body><a>tag</a><b>bold</b></body>"
    parser = og_scraper.OGParser()
    parser.feed(html)
    tag_count = parser.total_tag_count()
    assert tag_count == 3

def test_top_tags():
    html = "<a></a><a></a><a></a><b></b><b></b><c/>"
    parser = og_scraper.OGParser()
    parser.feed(html)
    top_tags = parser.top_tags(2)
    assert top_tags == [('a', 3), ('b', 2)]
