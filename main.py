import requests
from fake_headers import Headers
import json
from bs4 import BeautifulSoup
import re


headers = Headers(browser="firefox", os='win')
headers_data = headers.generate()

src = requests.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2", headers=headers_data).text
soup = BeautifulSoup(src, "lxml")
# pattern = re.compile('(.*[Dd]jango.*[Ff]lask.*)|(.*[Ff]lask.*[Dd]jango.*)')
pattern = re.compile('(.*[Dd]jango.*)|(.*[Ff]lask.*)')
vac_list = soup.find_all("div", class_='vacancy-serp-item__layout')
jsons = []
for vacancy in vac_list:
    vacancy_text = requests.get(vacancy.find_next('a')['href'], headers=headers_data).text
    soup2 = BeautifulSoup(vacancy_text, 'lxml')
    plain_text = soup2.find('div', class_='g-user-content')
    if plain_text is not None and pattern.match(plain_text.text):
        ref = vacancy.find_next('a')['href']
        salary = vacancy.find_next("span", class_='bloko-header-section-2')
        company = vacancy.find_next("a", class_='bloko-link bloko-link_kind-tertiary').text
        city = vacancy.find_next('div', attrs={"data-qa": 'vacancy-serp__vacancy-address'}).text
        if salary is not None:
            prepared_json = {"ref": ref, "salary": salary.text, "company": company, "city": city}
        else:
            prepared_json = {"ref": ref, "salary": "Undefined", "company": company, "city": city}
        jsons.append(prepared_json)


with open("sample.json", "w", encoding='utf8') as f:
    json.dump(jsons, f, ensure_ascii=False, indent=2)

