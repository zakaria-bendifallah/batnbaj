
import re

def add_new_line(text):
    text = text.replace("\n","<br>")
    return text

def add_url_tags(text):

    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    for url in urls:
       text = text.replace(url, "<a href={}>{}</a>".format(url,url))      
    
    return text
