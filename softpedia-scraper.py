import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# prepare the option for the chrome driver
options = webdriver.FirefoxOptions()
options.add_argument('-headless')

path = os.path.join(os.getcwd(), 'geckodriver.exe')
print(path)

# start chrome browser
browser = webdriver.Firefox(executable_path=path, options=options)
# browser.get("https://www.softpedia.com/get/Antivirus/Avast-Home-Edition.shtml")
# browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/h3[3]').click()
# print(browser.page_source)

# url = 'https://www.softpedia.com/catList/41,0,1,0,{}.html'
# url = 'https://www.softpedia.com/catList/29,0,1,0,{}.html'
# 'https://www.softpedia.com/catList/22,0,1,0,{}.html'
url = 'https://www.softpedia.com/catList/1,0,1,0,{}.html'

filename = 'file-sharing-features.txt'

count = 0

# with open(filename, 'w') as f:
for i in range(1, 20):

    r = requests.get(url.format(i))

    if r.status_code != 200:
        print('can\'t retrieve the html!')
        exit(1)

    soup = BeautifulSoup(r.content, 'lxml')

    # d = {}

    app_items = soup.select('div.grid_48.dlcls')

    summary = []  # summary of features
    details = []  # details of features

    for item in app_items:
        link = item.find('h4', class_='ln').find('a')['href']
        app_name = link[link.rfind('/')+1:len(link)].replace('.shtml', '')

        browser.get(link)
        try:
            browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/h3[3]').click()
        except Exception:
            continue
        soup = BeautifulSoup(browser.page_source, 'lxml')

        specs = soup.find(id='specifications')
        # changelogs = soup.find('span', class_='changelog').find_all('ul', recursive=False)

        changes = specs.select('b.upcase.bold')
        found_feature = False
        for c in changes:
            if c.text == 'features':
                print('found feature!')
                features = c.find_next('ul')
                found_feature = True
                count += 1
                break

        if found_feature is False:
            continue

            # changelogs = soup.find('span', class_='changelog').find_all('ul', recursive=False)
            #
            # l = len(changelogs)
            # if l == 1:
            #     features = changelogs[0]
            # elif l == 3:
            #     features = changelogs[1]
            # else:
            #     print('features len = {}'.format(l))
            #     print(changelogs)
            #     continue

            # descriptions = features.find_all('li')
            # for d in descriptions:
            #     print(d.text)
            #     if d.has_attr('class') is False:
            #         try:
            #             f.write(d.text + '\n')
            #         except UnicodeEncodeError as e:
            #             continue

                # if d.has_attr('class'):
                #     summary.append(d.text)
                # else:
                #     details.append(d.text)
#
# with open('summary.txt', 'w') as f:
#     for s in summary:
#         f.write(s + '\n')
#
# with open('details.txt', 'w') as f:
#     for d in details:
#         f.write(d + '\n')

# print(len(l))

print(count)