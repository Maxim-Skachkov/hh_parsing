from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
import time

from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless")
browser_path = Service(r"C:\Users\sklad\PycharmProjects\django_parsing_HH.ru\hh_parse\parser\bs4_parsing\chromedriver\chromedriver.exe".replace("\\", "/"))
browser = webdriver.Chrome(service=browser_path, options=options)


def get_right_link(job_name: str) -> str:
    """
    Определяет URL, который HH.ru присвоит запросу в поисковой строке
    :param job_name:
    Содержит ключевые слова по вакансии или ее название
    :return:
    URL
    """
    url = "https://spb.hh.ru/"
    try:
        browser.get(url=url)
        time.sleep(0.2)
        job_name_input = browser.find_element(by=By.ID, value="a11y-search-input")
        job_name_input.clear()
        job_name_input.send_keys(job_name)
        time.sleep(0.23)
        job_name_input.send_keys(Keys.ENTER)
        # enter_button_class = "bloko-button bloko-button_kind-primary bloko-button_scale-large bloko-button_stretched"
        # enter_button = browser.find_element(By.XPATH, value=f"//button[@class='{enter_button_class}']")
        # enter_button.click()
        # time.sleep(0.03)
        return browser.current_url
    except Exception as e:
        print(e)
        return ''
    finally:
        browser.close()
        browser.quit()


if __name__ == '__main__':
    print(get_right_link('Танцор диско'))