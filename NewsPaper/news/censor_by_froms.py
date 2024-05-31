from django import template
import requests
from bs4 import BeautifulSoup as BS

register = template.Library()

url = "http://argon.pro/humor/dict"
response = requests.get(url)
soup = BS(response.text, 'lxml')
words = soup.find_all("p")
bad_words_list = []
for word in words:
    word = str(word)
    bad_word = word.replace("<p>", "")
    bad_word_ = bad_word.split()[0]
    if len(bad_word_) <= 2 or (bad_word_ == "ИГРА") or (bad_word_ == "ИГРЫ"):
        pass
    else:
        bad_words_list.append(bad_word_)

bad_words_list.append("ЕБАЛ")
bad_words_list.append("ПИЗДЫ")
bad_words_list.append("ХУЯ")

