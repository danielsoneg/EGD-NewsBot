#!/usr/bin/env python
#! encoding: utf-8
from evwrapper import Evernote
import requests
import sys

from bs4 import BeautifulSoup as bs4
from readability.readability import Document


def evernotify(html, url):
  doc = Document(html, url=url)
  html = doc.summary()
  allowed_tags = ['a', 'abbr', 'acronym', 'address', 'area', 'b', 'bdo', 'big', 'blockquote', 'br', 'caption', 'center', 'cite', 'code', 'col', 'colgroup', 'dd', 'del', 'dfn', 'div', 'dl', 'dt', 'em', 'font', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 'ins', 'kbd', 'li', 'map', 'ol', 'p', 'pre', 'q', 's', 'samp', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th', 'thead', 'title', 'tr', 'tt', 'u', 'ul', 'var', 'xmp']
  disallowed_attrs = ['id', 'class', 'onclick', 'ondblclick', 'accesskey', 'data', 'dynsrc', 'tabindex', 'content']
  soup = bs4(html)
  body = soup.body
  body.name = "en-note"
  pid = 0
  for tag in body.find_all(lambda b: True, recursive=True):
    if tag.name not in allowed_tags:
      tag.name = "span"
    for attr in filter(lambda d: tag.attrs.get(d, False), disallowed_attrs):
      del(tag[attr])
    for attr in filter(lambda a: a.startswith('item'), tag.attrs.keys()):
      del(tag[attr])
  body = body.prettify()
  body = '<?xml version="1.0" encoding="UTF-8"?>\n\
      <!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">\n%s' % body
  body = body.encode('utf-8')
  print body
  return doc.short_title(), body

def main():
  url = "".join(sys.argv[1:])
  r = requests.get(url)
  title, body = evernotify(r.text, url)
  ev = Evernote()
  print ev.makeNote(title, body, url).guid

if __name__ == "__main__":
  main()
