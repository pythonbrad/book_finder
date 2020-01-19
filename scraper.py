# -*- coding: utf-8 -*-
import requests as r

class Scraper:
    """
        Eg:
        d="<html><body><p>Hello</p><p>World</p></body></html>"
        >>> s=Scraper()
        >>> s.find_tag('<p>', '</p>', count=1)
        Hello
        >>> s.find_tag('<p>', '</p>', count=1, with_tag=1)
        <p>Hello</p>
    """
    def __init__(self):
        #should be encoded
        self.data = b""
    def load_file(self, filename):
        file = open(filename, 'rb')
        self.data = file.read()
        file.close()
    def load_url(self, url, params={}):
        req = r.get(url, params=params)
        if req.status_code == 200:
            self.data = req.content
        else:
            self.data = b''
        req.close()
    def find_tag(self, start_tag, end_tag, count=-1, with_tag=0):
        start_index = 0
        end_index = len(self.data)
        result = []
        #We verify if data can be scraped
        if end_index != 0:
            i = 0
            while(start_index != -1 and (i < count+1 or count == -1)):
                start_index = self.data.find(start_tag, start_index)
                end_index = self.data.find(end_tag, start_index+len(start_tag))+len(end_tag)
                if (start_index == -1 or end_index == -1):
                    #no data scaped
                    break;
                #get data
                s = Scraper()
                #if with_tag, we get data begin by the start_tag to end_tag
                #else after the start_tag to before the end_tag
                a = start_index+len(start_tag) if not with_tag else start_index
                b = end_index-len(end_tag) if not with_tag else end_index
                #We get data
                s.data = self.data[a:b]
                #Renitiation start_index
                start_index = end_index
                #save data
                result.append(s)
                #increment count
                i+=1
        if not result:
            #To evit some error
            result = [Scraper()]
        return result
