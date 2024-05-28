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
    if len(bad_word_) <= 2:
        pass
    else:
        bad_words_list.append(bad_word_)

bad_words_list.append("ЕБАЛ")
bad_words_list.append("ПИЗДЫ")
bad_words_list.append("ХУЯ")

@register.filter()
def check_bad_words(text_post):
    text = str(text_post)
    for word1 in text.split():
        if word1.upper() in bad_words_list:
            text = text.replace(word1[1:], '*' * (len(word1)-1))
    return "".join(text)
