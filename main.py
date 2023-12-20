import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import json

file_path = "jobs.json"
url = "https://www.govtjobslive.com/government-jobs.html"

MY_EMAIL = "yunoastha3@gmail.com"
MY_PASSWORD = "rgnjfotowrqpenoe"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,te;q=0.8",
}
res = requests.get(url=url, headers=headers)
# print(price_head)
s2 = BeautifulSoup(res.text, 'html.parser')

cat_a = ['doctors', 'physicians', 'surgeons', 'anesthesiologists', 'etc.', 'engineers', 'software engineers',
         'civil engineers', 'mechanical engineers', 'etc.', 'lawyers', 'advocates', 'judges', 'legal advisors', 'etc.',
         'scientists', 'research scientists', 'biochemists', 'physicists', 'etc.', 'professors',
         'university professors', 'college lecturers', 'educators', 'etc.', 'senior managers', 'ceos', 'directors',
         'department heads', 'etc.', 'chartered accountants', 'financial auditors', 'tax consultants',
         'investment advisors', 'etc.']
cat_b = ['technicians', 'medical technicians', 'laboratory technicians', 'computer technicians', 'etc.', 'mechanics',
         'automobile mechanics', 'aircraft mechanics', 'machine repair technicians', 'etc.', 'supervisors',
         'production supervisors', 'team leaders', 'shift supervisors', 'etc.', 'data entry operators', 'data analysts',
         'medical coders', 'transcriptionists', 'etc.', 'customer service representatives', 'call center agents',
         'receptionists', 'sales representatives', 'etc.', 'accountants', 'junior accountants', 'bookkeepers',
         'payroll clerks', 'etc.', 'nurses', 'registered nurses', 'licensed practical nurses', 'nurse practitioners',
         'etc.']
cat_c = ['clerks', 'data entry clerks', 'filing clerks', 'administrative assistants', 'etc.', 'assembly line workers',
         'manufacturing workers', 'packaging workers', 'quality control inspectors', 'etc.', 'drivers', 'bus drivers',
         'taxi drivers', 'delivery drivers', 'etc.', 'agricultural workers', 'farmers', 'horticulture workers',
         'livestock handlers', 'etc.', 'security guards', 'security guards', 'airport security personnel',
         'traffic wardens', 'etc.', 'cashiers', 'bank tellers', 'shop cashiers', 'supermarket cashiers', 'etc.',
         'waiters and waitresses', 'restaurant servers', 'catering staff', 'baristas', 'etc.']
cat_d = ['sweepers', 'street sweepers', 'janitors', 'cleaners', 'etc.', 'gardeners', 'groundskeepers', 'landscapers',
         'gardeners', 'etc.', 'porters', 'hotel porters', 'baggage handlers', 'security guards', 'etc.', 'messengers',
         'office messengers', 'delivery boys', 'couriers', 'etc.']

jobs = s2.find_all(name='tbody')[1:]
data = []
try:
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
except:
    data = []


def posts(s):
    li = []
    x = ''
    for i in s:
        if i == ' ' or i == ',':
            if x:
                li.append(x.lower())
            x = ''
        else:
            x += i

    return li


for i in jobs:
    for j in i.find_all('tr')[1:]:

        d = {}
        d["img"] = "#"
        d["organisation"] = j.find_all('td')[1].text
        d["lastDate"] = j.find_all('td')[5].text
        d["role"] = "public"
        try:
            x = j.find_all('td')[2].find(name="strong").text.split('â\x80\x93')
        except:
            continue
        if len(x) == 2:

            d["post"] = x[0]
            if len(x[1].split()) == 2:
                d["vacancies"] = x[1].split()[0]
            else:
                continue
            try:
                d["link"] = j.find_all('td')[2].find(name="a")["href"]
            except:
                continue

            for i in posts(x[0]):
                i = i.lower()
                if i in cat_a:
                    d["cat"] = "A"
                    break
                elif i in cat_b:
                    d["cat"] = "B"
                    break
                elif i in cat_c:
                    d["cat"] = "C"
                    break

                elif i in cat_d:
                    d["cat"] = "D"
                    break

                else:
                    d["cat"] = "E"
                    break

        else:
            continue
        if d not in data:
            data.append(d)
        # print(j.find_all('td')[3].text, j.find_all('td')[6].text )

# EEnadu website:

url = "https://pratibha.eenadu.net/notifications/latestnotifications/private-jobs/2-8-29"
# u should pass headers in response to access full html code of the url site
response = requests.get(url=url, headers=headers)

price_head = response.text
# print(price_head)
soup = BeautifulSoup(price_head, 'html.parser')


# print(soup.prettify())
# Extract href link

#
#
#
def translate_text(text, source_language='te', target_language='en'):
    translator = Translator()
    translation = translator.translate(text, src=source_language, dest=target_language)
    return translation.text


def link(URL):
    # u should pass headers in response to access full html code of the url site
    res = requests.get(url=URL, headers=headers)
    # print(price_head)
    s2 = BeautifulSoup(res.text, 'html.parser')
    data = s2.find(name="div", class_="download-notice")
    return data.li.find_all(name='a')[-1]['href']


for i in soup.find(name='tbody').find_all(name='tr'):
    d = {
        "img": "#",
        "organisation": translate_text(i.find_all(name="td")[0].text, source_language="te", target_language="en"),
        "post": translate_text(i.find_all(name="td")[1].text, source_language="te", target_language="en"),
        "lastDate": i.find_all(name="td")[3].text,
        "link": link(i.find_all(name='td')[4].find(name='a')['href']),
        "role": "public",
        "vacancies": ""
    }
    for i in posts(d["post"]):
        i = i.lower()
        if i in cat_a:
            d["cat"] = "A"
            break
        elif i in cat_b:
            d["cat"] = "B"
            break
        elif i in cat_c:
            d["cat"] = "C"
            break
        elif i in cat_d:
            d["cat"] = "D"
            break

        else:
            d["cat"] = "E"
            break

    if d not in data:
        data.append(d)

# Write the data to the JSON file
with open(file_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)
    print('Success')

