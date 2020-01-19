# -*- coding: utf-8 -*-
from scraper import Scraper

"""
source:
    https://www.pdfdrive.com
    http://www.allitebooks.org
Exemple:
    finder = Finder()
    finder.pdfdrive("Human Biology")
    print(result)
    finder.result = []
    finder.allitebooks("Human Biology")
    print(result)
"""

class Finder:
    def __init__(self):
        self.result = []
        self.max_page = 3
    #Browse in https://www.pdfdrive.com
    def pdfdrive(self, search):
        scrap = Scraper()
        for page in range(1, self.max_page):
            scrap.load_url("https://www.pdfdrive.com/search", params={"q":search, "page":page})
            s1 = scrap.find_tag(b'<div class="file-left">',b'</div>')
            if s1[0].data:
                for i in s1:
                    d = {}
                    d["IMG_THUMBS"] = i.find_tag(b'src="',b'"', count=1)[0].data
                    d["IMG"] = i.find_tag(b'data-original="',b'"', count=1)[0].data
                    d["TITLE"] = i.find_tag(b'title="',b'"', count=1)[0].data
                    d["URL"] = b'https://www.pdfdrive.com'+i.find_tag(b'href="',b'"', count=1)[0].data
                    d["DATA_ID"] = i.find_tag(b'data-id="',b'"', count=1)[0].data
                    s2 = scrap.find_tag(b'<div class="file-info" data-id="%s">'%d["DATA_ID"], b'</div>', count=1)[0]
                    d["NB_PAGES"] = s2.find_tag(b'<span class="fi-pagecount ">', b'</span>', count=1)[0].data
                    d["YEAR"] = s2.find_tag(b'<span class="fi-year ">', b'</span>', count=1)[0].data
                    d["SIZE"] = s2.find_tag(b'<span class="fi-size hidemobile">', b'</span>', count=1)[0].data
                    d["NB_DOWNLOAD"] = s2.find_tag(b'<span class="fi-hit"', b'</span>', count=1)[0].data
                    d["SEARCH"] = search.encode()
                    d["LOCATE_PAGE"] = str(page).encode()
                    self.result.append(d)
            else:
                break
    #Browse in http://www.allitebooks.org
    def allitebooks(self, search):
        scrap = Scraper()
        for page in range(1, self.max_page):
            scrap.load_url("http://www.allitebooks.org/page/%s/"%page, params={"s":search})
            s1 = scrap.find_tag(b'<article',b'</article>')
            if s1[0].data:
                for i in s1:
                    d = {}
                    d["URL"] = i.find_tag(b'<a href="', b'"', count=1)[0].data
                    d["IMG"] = i.find_tag(b'src="', b'"', count=1)[0].data
                    d["TITLE"] = i.find_tag(b'alt="', b'"', count=1)[0].data
                    s2 = i.find_tag(b'<div class="entry-summary">', b'</div>', count=1)[0]
                    d["DESCRIPTION"] = s2.find_tag(b'<p>', b'</p>', count=1)[0].data
                    d["SEARCH"] = search.encode()
                    d["LOCATE_PAGE"] = str(page).encode()
                    self.result.append(d)
            else:
                break
