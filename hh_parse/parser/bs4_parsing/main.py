from bs4 import BeautifulSoup
import requests
import lxml
import fake_useragent
import time
from hh_parse.parser.bs4_parsing.chromedriver.main_selenium import get_right_link
from pprint import pprint


def get_links(job_name: str) -> list:
    ua = fake_useragent.UserAgent()
    url = get_right_link(job_name)
    data = requests.get(url, headers={'user-agent': ua.random})
    if data.status_code != 200:
        raise PermissionError('Что-то пошло не так')
    soup = BeautifulSoup(data.content, 'lxml')
    try:
        pagination_max_page = int(soup.find(
            "div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find("span").text)
        links = [fr"{url}&page={i}" for i in range(pagination_max_page)]
    except Exception as e:
        return []
    return links


pprint(get_links('Петрович менеджер'))

