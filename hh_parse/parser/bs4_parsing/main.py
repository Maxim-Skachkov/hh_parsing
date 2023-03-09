from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests
import fake_useragent
from hh_parse.parser.bs4_parsing.chromedriver.main_selenium import get_right_link
from pprint import pprint
import re


@dataclass
class VacancyInfo:
    job_name: str
    salary_min: int
    salary_max: int
    salary_tax: str
    job_experience: str
    company_name: str
    job_description: str
    key_skills: list[str]


def get_soup_via_url(url: str) -> BeautifulSoup:
    ua = fake_useragent.UserAgent()
    data = requests.get(url, headers={'user-agent': ua.random})
    if data.status_code != 200:
        raise PermissionError(f'Что-то пошло не так, url={url}')
    return BeautifulSoup(data.content, 'lxml')


def get_links(job_name: str) -> list:
    url = get_right_link(job_name)
    soup = get_soup_via_url(url)

    try:
        pagination_max_page = int(soup.find(
            "div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find("span").text)
        links = [fr"{url}&page={i}" for i in range(pagination_max_page)]
    except Exception as e:
        print(e)
        return []
    return links


def add_vacancy_to_db(vacancy: VacancyInfo) -> None:
    pass  # todo доработать запись в постргес


def vacancy_parsing(url: str) -> VacancyInfo:
    soup = get_soup_via_url(url)

    job_name = soup.find("h1", attrs={"data-qa": "vacancy-title"}).text
    salary = soup.find("div", attrs={"data-qa": "vacancy-salary"}).find("span").text
    salary = salary.replace(" ", "")
    if salary == "з/п не указана":
        salary_min = salary_max = salary_tax = None
    else:
        pattern = r'[\d ]{2,}'
        match = re.findall(pattern, salary)
        if len(match) == 1:
            salary_min, salary_max = int(match[0]), None
        else:
            salary_min, salary_max = int(match[0]), int(match[1])
        salary_tax = salary.split('руб. ')[-1]
    job_experience = soup.find("span", attrs={"data-qa": "vacancy-experience"}).text
    company_name = soup.find("a", attrs={"data-qa": "vacancy-company-name"}).text
    key_skills = soup.find_all("div", attrs={"data-qa": "bloko-tag bloko-tag_inline skills-element"})
    key_skills = [skill.text for skill in key_skills]

    job_description_first_el = soup.find("div", attrs={"data-qa": "vacancy-description"}).next_element
    job_description = [job_description_first_el]
    job_description.extend([jd for jd in job_description_first_el.next_siblings if jd.text != ' '])
    job_description = '\n'.join(map(lambda descr: descr.text, job_description))
    vacancy = VacancyInfo(job_name, salary_min, salary_max, salary_tax, job_experience,
                          company_name, job_description, key_skills)

    add_vacancy_to_db(vacancy)
    return vacancy


if __name__ == '__main__':
    url1 = "https://spb.hh.ru/vacancy/77353829?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%80%D0%BE%D0%B2%D0%B8%D1%87%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80"
    url2 = "https://spb.hh.ru/vacancy/77660835?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%80%D0%BE%D0%B2%D0%B8%D1%87%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80"
    url3 = "https://spb.hh.ru/vacancy/77019684?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%80%D0%BE%D0%B2%D0%B8%D1%87%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80"
    url4 = "https://spb.hh.ru/vacancy/73571441?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%80%D0%BE%D0%B2%D0%B8%D1%87%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80"
    url5 = "https://spb.hh.ru/vacancy/73088194?from=main"
    url6 = "https://spb.hh.ru/vacancy/75558847?from=vacancy_search_list&query=%D1%82%D1%83%D0%B0%D0%BB%D0%B5%D1%82"
    vacancy_parsing(url1)

