from bs4 import BeautifulSoup
import json
from urllib.request import urlopen
import re as regex

drexel_json = { "colleges": [] }

def find(pred, iterable):
  for element in iterable:
      if pred(element): return element
  return None

def html(url):
    return BeautifulSoup(urlopen(url).read(), features = "html.parser")
