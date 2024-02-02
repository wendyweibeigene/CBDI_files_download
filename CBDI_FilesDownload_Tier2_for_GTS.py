# %%
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
from datetime import datetime, timedelta
import re
import os
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import warnings

from webdriver_manager.chrome import ChromeDriverManager

warnings.filterwarnings("ignore")

myheaders = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

dicts = {'FIRST': 'Q1', 'SECOND': 'Q2', 'THIRD': 'Q3', 'FOURTH': 'Q4'}


# %%
def get_EQRx_fr():
    url = 'https://investors.eqrx.com/news-events/events-presentations'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.get(url)
    browser.implicitly_wait(5)
    print('browser opened successfully!')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    div = soup.find('div', attrs={'class': 'latest-posts type-events'})
    for div_tag in div.find_all('div', attrs={'class': 'post type-events'}):
        if re.findall('Financial Results', div_tag.find(name='a').text.strip()):
            h = div_tag.find_all(name='a')[-1]
            year = div_tag.find(name='a').text.strip().split(' ')[1]
            output_dir = os.path.join('EQRx', year)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            quarter = div_tag.find(name='a').text.strip().split(' ')[0]
            myfile = requests.get('https://investors.eqrx.com' + h.get('href'), allow_redirects=True)
            open(os.path.join(output_dir, "EQRx {0} {1} {2}".format(quarter, year, 'Presentation') + '.pdf'),
                 'wb').write(myfile.content)
            break
    url = 'https://investors.eqrx.com/news-events/news-releases'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.get(url)
    browser.implicitly_wait(5)
    print('browser opened successfully!')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    articles = soup.find('ul', attrs={'class': 'alm-listing alm-ajax'}).find_all('a')
    for article in articles:
        if re.search(re.compile('Reports.*Financial Results'), article.text.strip()):
            link = article.get('href')
            soup_n = BeautifulSoup(requests.get('https://investors.eqrx.com/' + link).text)
            h = soup_n.find('div', attrs={'class': 'file-link pdf-file-link'}).find('a')
            myfile = requests.get('https://investors.eqrx.com/' + h.get('href'), allow_redirects=True)
            open(os.path.join(output_dir, "EQRx {0} {1} {2}".format(quarter, year, 'PR') + '.pdf'), 'wb').write(
                myfile.content)
            break
    return year, quarter


# %%
def get_Daiichi_fr():
    url = 'https://www.daiichisankyo.com/investors/library/quarterly_result/'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.get(url)
    browser.implicitly_wait(5)
    browser.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
    browser.find_element(By.XPATH, '//*[@id="d-mordalWrap"]/div[2]').click()
    print('browser opened successfully!')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    div = soup.find('div', attrs={'id': 'dnn_ctr1226_ModuleContent'})
    for table in div.find_all('table'):
        title = table.tbody.tr.text.strip()
        if re.search(re.compile('Announcement of.*Financial Results'), title):
            year = re.findall('\d\d\d\d', title)[0]
            quarter = title.split(' ')[4]
            output_dir = os.path.join('Daiichi Sankyo', year)
            hrefs = table.find_all('a')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            break
    if hrefs:
        for h in hrefs:
            if re.search('Financial Results', h.text.strip()):
                myfile = requests.get('https://www.daiichisankyo.com' + h.get('href'), allow_redirects=True)
                open(os.path.join(output_dir, "Daiichi Sankyo {0} {1} {2}".format(quarter, year, 'PR') + '.pdf'),
                     'wb').write(myfile.content)
            elif re.search('Reference Data', h.text.strip()):
                myfile = requests.get('https://www.daiichisankyo.com' + h.get('href'), allow_redirects=True)
                open(os.path.join(output_dir,
                                  "Daiichi Sankyo {0} {1} {2}".format(quarter, year, 'Reference Data') + '.pdf'),
                     'wb').write(myfile.content)
            elif re.search('Presentation Material', h.text.strip()):
                myfile = requests.get('https://www.daiichisankyo.com' + h.get('href'), allow_redirects=True)
                open(os.path.join(output_dir,
                                  "Daiichi Sankyo {0} {1} {2}".format(quarter, year, 'Presentation') + '.pdf'),
                     'wb').write(myfile.content)
            else:
                pass
    return year, quarter


# %%
def get_GSK_fr():
    url = 'https://www.gsk.com/en-gb/investors/quarterly-results/'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.set_page_load_timeout(50)
    try:
        browser.get(url)
        browser.implicitly_wait(5)
    except Exception:
        browser.execute_script('window.stop()')
    browser.find_element(By.XPATH, '//*[@id="preferences_prompt_submit"]').click()
    print('browser opened successfully!')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    # others
    div = soup.find_all('div', attrs={'class': 'download-list quarterly-results__downloads-inner'})[0]
    hrefs = div.find_all('a')
    year = hrefs[1].text.strip().split(' ')[1]
    quarter = hrefs[1].text.strip().split(' ')[0]
    output_dir = os.path.join('GSK', year)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for h in hrefs:
        backfix = '.' + h.get('href').split('.')[-1]
        name = h.text.strip().split('(')[0].strip()
        if re.search('epidemiology', name):
            myfile = requests.get('https://www.gsk.com' + h.get('href'), allow_redirects=True)
            open(os.path.join(output_dir, "GSK {0} {1} {2}".format(quarter, year, 'Epidemiology') + backfix),
                 'wb').write(myfile.content)
        elif re.search('results slides', name):
            myfile = requests.get('https://www.gsk.com' + h.get('href'), allow_redirects=True)
            open(os.path.join(output_dir, "GSK {0} {1} {2}".format(quarter, year, 'Presentation') + backfix),
                 'wb').write(myfile.content)
        elif re.search('trials report', name):
            myfile = requests.get('https://www.gsk.com' + h.get('href'), allow_redirects=True)
            open(os.path.join(output_dir, "GSK {0} {1} {2}".format(quarter, year, 'Trials Appendix') + backfix),
                 'wb').write(myfile.content)
        else:
            pass
    # pr
    div = soup.find_all('div', attrs={'class': 'quarterly-results__primary-content'})[0]
    hrefs = div.find_all('a')
    for h in hrefs:
        name = h.text.strip().split('(')[0].strip()
        if re.search('full results announcement', name):
            myfile = requests.get('https://www.gsk.com' + h.get('href'), allow_redirects=True)
            open(os.path.join(output_dir, "GSK {0} {1} {2}".format(quarter, year, 'PR') + '.pdf'), 'wb').write(
                myfile.content)
    return year, quarter


# %%
def get_JNJ_fr():
    url = 'https://johnsonandjohnson.gcs-web.com/financial-information/quarterly-results'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.set_page_load_timeout(50)
    try:
        browser.get(url)
        browser.implicitly_wait(5)
    except Exception:
        browser.execute_script('window.stop()')
    print('browser opened successfully!')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    div = soup.find('div', attrs={'class': 'quarters-wrapper'}).div
    year = soup.find('div', attrs={'class': 'module-financial_year-text'}).text.strip()
    quarter = div.h4.text.strip()
    output_dir = os.path.join('JNJ', year)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    hrefs_ = div.find_all('a')
    for h in hrefs_:
        if re.search('Press Release', h.text.strip()):
            myfile = requests.get(h.get('href'), allow_redirects=True, headers=myheaders)
            open(os.path.join(output_dir, "JNJ {0} {1} {2}".format(quarter, year, 'PR') + '.pdf'), 'wb').write(
                myfile.content)
        elif re.search('Presentation', h.text.strip()):
            myfile = requests.get(h.get('href'), allow_redirects=True, headers=myheaders)
            open(os.path.join(output_dir, "JNJ {0} {1} {2}".format(quarter, year, 'Presentation') + '.pdf'),
                 'wb').write(myfile.content)
        else:
            pass
    return year, quarter


# %%
def get_Genmab_fr():
    dicts = {'first quarter': 'Q1', 'first half': 'Q2', 'first nine': 'Q3', 'annual': 'Q4'}
    url = 'https://ir.genmab.com/events-and-presentations'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.set_page_load_timeout(50)
    try:
        browser.get(url)
        browser.implicitly_wait(5)
    except Exception:
        browser.execute_script('window.stop()')
    print('browser opened successfully!')
    browser.find_element(By.XPATH,
                         '//*[@id="block-nir-pid2351-content"]/article/div/div/div/div/div/div[1]/div/ul/li[2]').click()
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    articles = soup.find_all('article', attrs={
        'class': 'clearfix node node--nir-event--nir-widget-list node--type-nir-event node--view-mode-nir-widget-list'})
    for a in articles:
        title = a.find('div', attrs={'class': 'nir-widget--field nir-widgets--event--title'}).text.strip()
        if re.findall(re.compile('Publication of the (.*)\d\d\d\d'), title):
            sup = a.find('div', attrs={'class': 'nir-widget--field nir-widget--event--support-materials'})
            if sup:
                year = re.findall('\d\d\d\d', title)[0]
                for q in ['first quarter', 'first half', 'first nine', 'annual']:
                    if re.search(q, title.lower()):
                        quarter = dicts[q]
                hrefs_ = sup.find_all(name='a')
                output_dir = os.path.join('Genmab', year)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                break
            else:
                continue
    if hrefs_:
        for h in hrefs_:
            if re.search('Interim Report', h.text.strip()):
                myfile = requests.get('https://ir.genmab.com' + h.get('href'), allow_redirects=True)
                open(os.path.join(output_dir, "Genmab {0} {1} {2}".format(quarter, year, 'PR') + '.pdf'), 'wb').write(
                    myfile.content)
            elif re.search('Presentation', h.text.strip()):
                myfile = requests.get('https://ir.genmab.com' + h.get('href'), allow_redirects=True)
                open(os.path.join(output_dir, "Genmab {0} {1} {2}".format(quarter, year, 'Presentation') + '.pdf'),
                     'wb').write(myfile.content)
            else:
                pass
    return year, quarter


# %%
def get_Incyte_fr():
    url = 'https://investor.incyte.com/financials/quarterly-results'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.set_page_load_timeout(50)
    try:
        browser.get(url)
        browser.implicitly_wait(5)
    except Exception:
        browser.execute_script('window.stop()')
    print('browser opened successfully!')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    # browser.quit()
    div = soup.find_all('div', attrs={'class': re.compile('owl-item.*')})[0]
    # owl-item active
    li_tags = div.find_all('li', attrs={'class': 'views-row'})
    year = div.div.h2.text
    output_dir = os.path.join('Incype', year)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # PR
    pres = li_tags[0]
    h = pres.find_all(name='a')[-1]
    quarter = h.text
    res = requests.get('https://investor.incyte.com' + h.get('href'), headers=myheaders)
    soup_2 = BeautifulSoup(res.text, 'lxml')
    h = soup_2.find('div', attrs={'class': 'file-link pdf-file-link'}).find(name='a')
    myfile = requests.get('https://investor.incyte.com' + h.get('href'), allow_redirects=True)
    open(os.path.join(output_dir, "Intype {0} {1} {2}".format(quarter, year, 'PR') + '.pdf'), 'wb').write(
        myfile.content)
    time.sleep(3)
    # presentation
    ppt = li_tags[1]
    h = ppt.find_all(name='a')[-1]
    myfile = requests.get('https://investor.incyte.com' + h.get('href'), allow_redirects=True)
    open(os.path.join(output_dir, "Intype {0} {1} {2}".format(quarter, year, 'Presentation') + '.pdf'), 'wb').write(
        myfile.content)
    time.sleep(3)
    return year, quarter


# %%
def get_Regeneron_fr():
    url = 'https://investor.regeneron.com/financial-information/quarterly-results'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')
    # 实例化Chrome driver
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.get(url)
    time.sleep(3)
    print('browser opened successfully!')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    div = soup.find_all('div', attrs={'class': 'view-grouping'})[0]
    div_tag = div.find_all('div', attrs={'class': 'views-row'})[0]
    year = div.h2.text
    quarter = div.find_all('div', attrs={'class': 'row'})[0].h3.text
    # hrefs_ = div_tag.find_all(name='a')[1:]
    hrefs_ = div_tag.find_all(name='a')
    output_dir = os.path.join('Regeneron', year)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for h in hrefs_[:2]:
        name = ''
        if ("Presentation" in str(h)):
            name = "Presentation"
        elif ("Regeneron" in str(h)):
            name = "Press Release"
        else:
            pass
        if h.get('type'):
            myfile = requests.get('https://investor.regeneron.com' + h.get('href'), allow_redirects=True)
            open(os.path.join(output_dir, 'Regeneron {1} {0} {2}'.format(year, quarter, name) + '.pdf'), 'wb').write(
                myfile.content)
        else:
            link = 'https://investor.regeneron.com' + h.get('href')
            res = requests.get(link)
            soup_2 = BeautifulSoup(res.text, 'lxml')
            h = soup_2.find_all('div', attrs={'class': 'ml-4'})[0].find(name='a')
            myfile = requests.get('https://investor.regeneron.com' + h.get('href'), allow_redirects=True)
            open(os.path.join(output_dir, 'Regeneron {1} {0} {2}'.format(year, quarter, name) + '.pdf'), 'wb').write(
                myfile.content)
    # %%
    return year, quarter


# %%
def get_Takeda_fr():
    url = 'https://www.takeda.com/investors/financial-results/quarterly-results/'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.set_page_load_timeout(50)
    try:
        browser.get(url)
        browser.implicitly_wait(5)
    except Exception:
        browser.execute_script('window.stop()')
    print('browser opened successfully!')
    browser.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    div = soup.find_all('section')[2]
    year = soup.find_all('section')[1].div.h2.text[2:6]
    quarter = 'Q' + div.div.div.text[-1]
    hrefs_ = div.find_all(name='a')
    output_dir = os.path.join('Takeda', year)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for h in hrefs_:
        if ("Presentation" in h.text.strip()):
            name = 'Earnings Presentation'
            myfile = requests.get(h.get('href'), allow_redirects=True)
            open(os.path.join(output_dir, 'Takeda {1} {0} {2}'.format(year, quarter, name) + '.pdf'), 'wb').write(
                myfile.content)
    return year, quarter


# %%
def get_HutchMed_fr():
    dicts = {'half-year': 'H1', 'full': 'FY'}
    url = 'https://www.hutch-med.com/shareholder-information/event-information/'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.set_page_load_timeout(50)
    try:
        browser.get(url)
        browser.implicitly_wait(5)
    except Exception:
        browser.execute_script('window.stop()')
    print('browser opened successfully!')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    div = soup.find_all('div', attrs={'class': 'event-block row'})
    for div_tag in div:
        if re.search('Financial Results', div_tag.span.text.strip()):
            year = div_tag.span.text.strip().split(' ')[0]
            quarter = div_tag.span.text.strip().split(' ')[1]
            quarter = dicts[quarter.lower()]
            link = div_tag.find_all('a')[0].get('href')
            break
    output_dir = os.path.join('HutchMed', year)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    res = requests.get(link, headers=myheaders)
    soup_2 = BeautifulSoup(res.text, 'lxml')
    count = 0
    hrefs_ = soup_2.find('div', attrs={'class': 'attachments'}).find_all(name='a')
    for h in hrefs_:
        count += 1
        myfile = requests.get(h.get('href'), allow_redirects=True)
        open(os.path.join(output_dir, 'HutchMed {1} {0} {2}'.format(year, quarter, 'Report-EN') + '.pdf'), 'wb').write(
            myfile.content)
        # presentation
    url = div_tag.find_all('a')[1].get('href')
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.set_page_load_timeout(50)
    try:
        browser.get(url)
        browser.implicitly_wait(5)
    except Exception:
        browser.execute_script('window.stop()')
    print('browser opened successfully!')
    browser.find_element(By.ID, "input_965333").send_keys("lifen")
    browser.find_element(By.ID, "input_965334").send_keys("liu")
    browser.find_element(By.ID, "input_965335").send_keys("lifen.liu@beigene.com")
    browser.find_element(By.ID, "input_965336").send_keys("BeiGene")
    browser.find_element(By.XPATH,
                         '//*[@id="registration-switcher-form-guestbook"]/div[2]/app-accessible-submit/button').click()
    browser.find_element(By.XPATH, '//*[@id="mainMenu"]/ul/li[3]').click()
    soup = BeautifulSoup(browser.page_source, 'lxml')
    h = soup.find('div', attrs={'class': 'clearfix'}).find('a')
    browser.quit()
    myfile = requests.get(h.get('href'), allow_redirects=True)
    open(os.path.join(output_dir, 'HutchMed {1} {0} {2}'.format(year, quarter, 'Presentation-EN') + '.pdf'),
         'wb').write(myfile.content)

    return year, quarter


# %%
def get_junshi_fr():
    dicts = {'中期': '1H', '年度': 'FY'}
    url = 'https://junshi-bioscience-v2-umb.azurewebsites.net/cn/investors/presentation-materials/'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.set_page_load_timeout(50)
    try:
        browser.get(url)
        browser.implicitly_wait(5)
    except Exception:
        browser.execute_script('window.stop()')
    print('browser opened successfully!')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    divs = soup.find_all('div', attrs={'class': 'pm-col'})
    for div in divs:
        if '业绩发布' in div.text.strip():
            year = re.findall('\d\d\d\d', div.text.strip())[0]
            for key in dicts:
                if re.search(key, div.text.strip()):
                    quarter = dicts[key]
            output_dir = os.path.join('Junshi', year)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            h = div.find('a')
            myfile = requests.get('https://junshi-bioscience-v2-umb.azurewebsites.net/' + h.get('href'),
                                  allow_redirects=True)
            open(os.path.join(output_dir, 'Junshi {0} {1} {2}'.format(quarter, year, 'Presentation-PR EN') + '.pdf'),
                 'wb').write(myfile.content)
            break
    url = 'https://junshi-bioscience-v2-umb.azurewebsites.net/cn/investors/announcements-and-circulars/'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.set_page_load_timeout(50)
    try:
        browser.get(url)
        browser.implicitly_wait(5)
    except Exception:
        browser.execute_script('window.stop()')
    print('browser opened successfully!')
    browser.switch_to.default_content()
    frame = browser.find_elements(By.TAG_NAME, 'iframe')[0]
    browser.switch_to.frame(frame)
    pages = browser.find_elements(By.XPATH, '//*[@id="PagesContainer"]/table/tbody/tr/td[2]')[0].text.strip()
    browser.find_elements(By.XPATH, '//*[@id="YearPeriodsContainer"]/a[6]')[0].click()
    dicts = {'第一季度': 'Q1', '中期': '1H', '第三季度': 'Q3', '全年': 'FY'}
    if 1:
        soup = BeautifulSoup(browser.page_source, 'lxml')
        divs = soup.find_all('div', attrs={'class': re.compile('PressRelease PressRelease*')})
        for div in divs:
            title = div.find('div', attrs={
                'class': 'PressRelease-SingleLine-DataColumn PressRelease-SingleLine-TitleContainer'}).text.strip()
            if re.findall(re.compile('君实生物.*季度报告'), title):
                year = re.findall('\d\d\d\d', title)[0]
                for key in dicts:
                    if re.search(key, title):
                        quarter = dicts[key]
                output_dir = os.path.join('Junshi', year)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                stop = True
                link = div.find_all(name='a')[0].get('href')
                soup_n = BeautifulSoup(requests.get('https://asia.tools.euroland.com/' + link).text)
                h = soup_n.find('div', attrs={'id': 'SeparateNews-Body'}).find('a')
                myfile = requests.get(h.get('href'), allow_redirects=True)
                open(os.path.join(output_dir, 'Junshi {0} {1} {2}'.format(quarter, year, 'Results-PR EN') + '.pdf'),
                     'wb').write(myfile.content)
                break
            else:
                stop = False
                continue
    if not stop:
        for i in range(1, len(pages)):
            xpath = '//*[@id="PagesContainer"]/table/tbody/tr/td[2]/a[{0}]'.format(i)
            browser.find_element(By.XPATH, xpath).click()
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, 'lxml')
            divs = soup.find_all('div', attrs={'class': re.compile('PressRelease PressRelease*')})
            for div in divs:
                title = div.find('div', attrs={
                    'class': 'PressRelease-SingleLine-DataColumn PressRelease-SingleLine-TitleContainer'}).text.strip()
                if re.findall(re.compile('君实生物.*季度报告'), title):
                    year = re.findall('\d\d\d\d', div.text)[0]
                    for key in dicts:
                        if re.search(key, title):
                            quarter = dicts[key]
                    output_dir = os.path.join('Junshi', year)
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    link = div.find_all(name='a')[0].get('href')
                    soup_n = BeautifulSoup(requests.get('https://asia.tools.euroland.com' + link).text)
                    h = soup_n.find('div', attrs={'id': 'SeparateNews-Body'}).find('a')
                    myfile = requests.get(h.get('href'), allow_redirects=True)
                    open(
                        os.path.join(output_dir, 'Junshi {0} {1} {2}'.format(quarter, year, 'Results -PR EN') + '.pdf'),
                        'wb').write(myfile.content)
                    break
            else:
                continue
            break
    browser.quit()
    return year, quarter


# %%
def get_Seagen_fr():
    import json
    url = 'https://investor.seagen.com/financial-information/quarterly-results/default.aspx'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.set_page_load_timeout(50)
    try:
        browser.get(url)
        browser.implicitly_wait(5)
    except Exception:
        browser.execute_script('window.stop()')
    print('browser opened successfully!')
    browser.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
    soup = BeautifulSoup(browser.page_source, 'lxml')
    year_title = soup.find('div', attrs={'class': 'module-financial-table_header'})
    year = year_title.text.strip()[:4]
    output_dir = os.path.join('Seagen', year)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    rows = soup.find_all('div', attrs={'class': 'module-financial-table_body-row'})
    PRs = \
        rows[0].find_all('div',
                         attrs={'class': 'module-financial-table_body-year slick-slide slick-current slick-active'})[
            0]
    presentations = \
        rows[2].find_all('div',
                         attrs={'class': 'module-financial-table_body-year slick-slide slick-current slick-active'})[
            0]
    QFs = \
        rows[3].find_all('div',
                         attrs={'class': 'module-financial-table_body-year slick-slide slick-current slick-active'})[
            0]
    hrefs_pre = presentations.find_all('a')
    hrefs_PR = PRs.find_all('a')
    hrefs_QF = QFs.find_all('a')
    if len(hrefs_pre):
        quarter = hrefs_pre[-1].text.strip()[:2]
        h = hrefs_pre[-1].get('href')
        myfile = requests.get(h, allow_redirects=True)
        open(os.path.join(output_dir, 'Seagen {0} {1} {2}'.format(quarter, year, 'Presentation') + '.pdf'), 'wb').write(
            myfile.content)
    if len(hrefs_QF):
        quarter = hrefs_QF[-1].text.strip()[:2]
        h = hrefs_QF[-1].get('href')
        myfile = requests.get(h, allow_redirects=True)
        open(os.path.join(output_dir, 'Seagen {0} {1} {2}'.format(quarter, year, '10 Q SEC Filing') + '.pdf'),
             'wb').write(myfile.content)
    if len(hrefs_PR):
        quarter = hrefs_PR[-1].text.strip()[:2]
        h = hrefs_PR[-1].get('href')
        browser = quit()
        chrome_options = webdriver.ChromeOptions()
        settings = {
            "recentDestinations": [{
                "id": "Save as PDF",
                "origin": "local",
                "account": ""
            }],
            "selectedDestinationId": "Save as PDF",
            "version": 2,
            "isHeaderFooterEnabled": False,
            "isCssBackgroundEnabled": True,
            "mediaSize": {
                "height_microns": 297000,
                "name": "ISO_A4",
                "width_microns": 210000,
                "custom_display_name": "A4"
            },
        }
        chrome_options.add_argument('--enable-print-browser')
        prefs = {
            'printing.print_preview_sticky_settings.appState': json.dumps(settings),
            'savefile.default_directory': output_dir
        }
        chrome_options.add_argument('--kiosk-printing')
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(h)
        driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
        driver.maximize_window()  # 浏览器最大化
        driver.execute_script(
            'document.title="Seagen {0} {1} {2}.pdf";window.print();'.format(quarter, year, 'PR'))
        driver.quit()
    return year, quarter


# %%
def get_Cstone_fr():
    dicts = {'Interim': '1H', 'Annual': 'FY'}
    # report_en
    url = 'https://www.cstonepharma.com/en/relation/report.html'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.set_page_load_timeout(50)
    try:
        browser.get(url)
        browser.implicitly_wait(5)
    except Exception:
        browser.execute_script('window.stop()')
    print('browser opened successfully!')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    div = soup.find('div', attrs={'class': 'right_list'})
    li_tags = div.find_all('li')
    for li in li_tags:
        year = li.text.strip().split(' ')[0]
        quarter = li.text.strip().split(' ')[1]
        if quarter in dicts.keys():
            quarter = dicts[quarter]
            output_dir = os.path.join('CStone', year)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            h = li.find('a')
            myfile = requests.get('https://www.cstonepharma.com/' + h.get('href'), allow_redirects=True)
            open(os.path.join(output_dir, "Cstone {0} {1} {2}".format(quarter, year, 'Reports-EN') + '.pdf'),
                 'wb').write(myfile.content)
            break
        else:
            continue
    # presentation_en
    browser.find_element(By.XPATH, '/html/body/div[8]/div/div/div[1]/ul/li[4]').click()
    soup = BeautifulSoup(browser.page_source, 'lxml')
    div = soup.find('div', attrs={'class': 'right_list'})
    li_tags = div.find_all('li')
    for li in li_tags:
        year = li.text.strip().split(' ')[0]
        quarter = li.text.strip().split(' ')[1]
        if quarter in dicts.keys():
            quarter = dicts[quarter]
            output_dir = os.path.join('CStone', year)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            h = li.find('a')
            myfile = requests.get('https://www.cstonepharma.com/' + h.get('href'), allow_redirects=True)
            open(os.path.join(output_dir, "Cstone {0} {1} {2}".format(quarter, year, 'Presentation-EN') + '.pdf'),
                 'wb').write(myfile.content)
            break
        else:
            continue
    dicts = {'中期': '1H', '年报': 'FY'}
    # report_cn
    url = 'https://www.cstonepharma.com/relation/report.html'
    try:
        browser.get(url)
        browser.implicitly_wait(5)
    except Exception:
        browser.execute_script('window.stop()')
    print('browser opened successfully!')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    div = soup.find('div', attrs={'class': 'right_list'})
    li_tags = div.find_all('li')
    for li in li_tags:
        year = li.text.strip()[:4]
        for key in dicts.keys():
            if key in li.text.strip():
                quarter = dicts[key]
                output_dir = os.path.join('CStone', year)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                h = li.find('a')
                myfile = requests.get('https://www.cstonepharma.com/' + h.get('href'), allow_redirects=True)
                open(os.path.join(output_dir, "Cstone {0} {1} {2}".format(quarter, year, 'Reports-CN') + '.pdf'),
                     'wb').write(myfile.content)
                break
        else:
            continue
        break
    # presentation_cn
    dicts = {'半年度': '1H', '年度': 'FY'}
    browser.find_element(By.XPATH, '/html/body/div[8]/div/div/div[1]/ul/li[4]').click()
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    div = soup.find('div', attrs={'class': 'right_list'})
    li_tags = div.find_all('li')
    for li in li_tags:
        year = li.text.strip()[:4]
        for key in dicts.keys():
            if key in li.text.strip():
                quarter = dicts[key]
                output_dir = os.path.join('CStone', year)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                h = li.find('a')
                myfile = requests.get('https://www.cstonepharma.com/' + h.get('href'), allow_redirects=True)
                open(os.path.join(output_dir, "Cstone {0} {1} {2}".format(quarter, year, 'Presentation-CN') + '.pdf'),
                     'wb').write(myfile.content)
                break
        else:
            continue
        break
    return year, quarter


# %%
def get_CSPC_fr():
    dicts = {'Annual': 'FY', 'Interim': 'H1'}
    url = 'https://www.cspc.com.hk/en/ir/reports.php'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.set_page_load_timeout(50)
    try:
        browser.get(url)
        browser.implicitly_wait(5)
    except Exception:
        browser.execute_script('window.stop()')
    print('browser opened successfully!')
    # report
    soup = BeautifulSoup(browser.page_source, 'lxml')
    year = soup.find('div', attrs={'class': 'year'}).find_all('li')[0].text
    output_dir = os.path.join('CSPC', year)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    finre = soup.find_all('div', attrs={'class': 'finreport'})[0]
    quarter = finre.text.strip().split(' ')[0]
    quarter = dicts[quarter]
    h = finre.find(name='a')
    myfile = requests.get(h.get('href'), allow_redirects=True)
    open(os.path.join(output_dir, "CSPC {0} {1} {2}".format(quarter, year, 'Reports-EN') + '.pdf'), 'wb').write(
        myfile.content)
    # presentation
    browser.find_element(By.XPATH, '//*[@id="leftNav"]/ul/li[7]').click()
    soup = BeautifulSoup(browser.page_source, 'lxml')
    year = soup.find('div', attrs={'class': 'year'}).find_all('li')[0].text
    output_dir = os.path.join('CSPC', year)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    finre = soup.find_all('div', attrs={'class': 'finreport'})[0]
    quarter = finre.text.strip().split(' ')[1]
    h = finre.find(name='a')
    myfile = requests.get('https://www.cspc.com.hk/en/ir' + h.get('href'), allow_redirects=True)
    open(os.path.join(output_dir, "CSPC {0} {1} {2}".format(quarter, year, 'Presentation-EN') + '.pdf'), 'wb').write(
        myfile.content)

    dicts = {'年度': 'FY', '中期': 'H1'}
    url = 'https://www.cspc.com.hk/sc/ir/reports.php?year=2023'
    # chrome_options = webdriver.ChromeOptions()
    # #chrome_options.add_argument('--headless')
    # # chrome_options.add_argument('window-size=1920x1080')
    # chrome_options.add_argument('--start-maximized')
    # browser=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    # browser.set_page_load_timeout(50)
    try:
        browser.get(url)
        browser.implicitly_wait(5)
    except Exception:
        browser.execute_script('window.stop()')
    print('browser opened successfully!')
    # report
    soup = BeautifulSoup(browser.page_source, 'lxml')
    year = soup.find('div', attrs={'class': 'year'}).find_all('li')[0].text
    output_dir = os.path.join('CSPC', year)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    finre = soup.find_all('div', attrs={'class': 'finreport'})[0]
    quarter = finre.text.strip()[:2]
    quarter = dicts[quarter]
    h = finre.find(name='a')
    myfile = requests.get(h.get('href'), allow_redirects=True)
    open(os.path.join(output_dir, "CSPC {0} {1} {2}".format(quarter, year, 'Reports-CN') + '.pdf'), 'wb').write(
        myfile.content)
    # presentation
    dicts = {'年度': 'FY', '上半年': 'H1', '三季度': 'Q3', '一季度': 'Q1'}
    browser.find_element(By.XPATH, '//*[@id="leftNav"]/ul/li[7]').click()
    soup = BeautifulSoup(browser.page_source, 'lxml')
    year = soup.find('div', attrs={'class': 'year'}).find_all('li')[0].text
    output_dir = os.path.join('CSPC', year)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    finre = soup.find_all('div', attrs={'class': 'finreport'})[0]
    quarter = finre.text.strip()[5:]
    quarter = dicts[quarter]
    h = finre.find(name='a')
    myfile = requests.get('https://www.cspc.com.hk/sc/ir' + h.get('href'), allow_redirects=True)
    open(os.path.join(output_dir, "CSPC {0} {1} {2}".format(quarter, year, 'Presentation-CN') + '.pdf'), 'wb').write(
        myfile.content)
    browser.quit()
    return year, quarter


# %%
def get_Hansoh_fr():
    dicts = {'ANNUAL': 'FY', 'INTERIM': 'H1'}
    url = 'https://www.hspharm.com/investment/performance-report.jsp?catId=18'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.set_page_load_timeout(50)
    try:
        browser.get(url)
        browser.implicitly_wait(5)
    except Exception:
        browser.execute_script('window.stop()')
    print('browser opened successfully!')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    events = soup.find('ul', attrs={'class': 'reports fix'})
    for li in events.find_all('li'):
        if 'REPORT' in li.text.strip():
            year = li.find('a').text.strip().split(' ')[-1]
            quarter = li.find('a').text.strip().split(' ')[0]
            quarter = dicts[quarter]
            output_dir = os.path.join('Hansoh', year)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            h = li.find('a')
            myfile = requests.get('https://www.hspharm.com/' + h.get('href'), allow_redirects=True)
            open(os.path.join(output_dir, "Hansoh {0} {1} {2}".format(quarter, year, 'Report-EN') + '.pdf'),
                 'wb').write(myfile.content)
            break
    for li in events.find_all('li'):
        if 'ANNOUNCEMENT' in li.text.strip():
            year = re.findall('\d\d\d\d', li.find('a').text.strip())[0]
            quarter = li.find('a').text.strip().split(' ')[0]
            quarter = dicts[quarter]
            output_dir = os.path.join('Hansoh', year)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            h = li.find('a')
            myfile = requests.get('https://www.hspharm.com/' + h.get('href'), allow_redirects=True)
            open(os.path.join(output_dir, "Hansoh {0} {1} {2}".format(quarter, year, 'PR-EN') + '.pdf'), 'wb').write(
                myfile.content)
            break
    browser.quit()
    return year, quarter


# %%
def get_Sanofi_fr():
    url = 'https://www.sanofi.com/en/investors/financial-results-and-events'
    res = requests.get(url, headers=myheaders)
    time.sleep(3)
    print('browser opened successfully!')
    soup = BeautifulSoup(res.text, 'lxml')
    div_root = soup.find('div', attrs={'class': 'dotcom-event-content-list MuiBox-root css-jqikz1'})
    div = div_root.find_all('div', attrs={
        'class': 'MuiGrid2-root MuiGrid2-direction-xs-row MuiGrid2-grid-mobile-4 MuiGrid2-grid-tablet-8 MuiGrid2-grid-desktop-12 css-h663uz-MuiGrid2-root'})[
        2]
    downloads_link = 'https://www.sanofi.com' + div.find('a').get('href')
    year = div.h3.text.strip().split(' ')[-2]
    output_dir = os.path.join('Sanofi', year)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    quarter = div.h3.text.strip().split(' ')[0]
    quarter = dicts[quarter.upper()]
    res_2 = requests.get(downloads_link, headers=myheaders)
    soup_2 = BeautifulSoup(res_2.text, 'lxml')
    div_2 = soup_2.find_all('div', attrs={
        'class': 'MuiGrid2-root MuiGrid2-direction-xs-row MuiGrid2-grid-mobile-4 MuiGrid2-grid-tablet-2 MuiGrid2-grid-desktop-3 css-afvoyr-MuiGrid2-root'})[
        -2]
    hrefs = div_2.find_all(name='a')
    ps = div_2.find_all('p')
    for idx, p_ in enumerate(ps):
        if re.search('Presentation', p_.text.strip()):
            h = hrefs[idx].get('href')
            myfile = requests.get('https://www.sanofi.com' + h, allow_redirects=True)
            open(os.path.join(output_dir, "Sanofi {0} {1} {2}".format(quarter, year, 'Presentation') + '.pdf'),
                 'wb').write(myfile.content)
        elif re.search('Press release: Solid', p_.text.strip()):
            link = hrefs[idx].get('href')
            soup_n = BeautifulSoup(requests.get('https://www.sanofi.com/' + link).text)
            h = soup_n.find('a', attrs={'class': 'elements-ds-twdzwl'})
            myfile = requests.get('https://www.sanofi.com' + h.get('href'), allow_redirects=True)
            open(os.path.join(output_dir, "Sanofi {0} {1} {2}".format(quarter, year, 'Press release') + '.pdf'),
                 'wb').write(myfile.content)
        else:
            continue
    return year, quarter


# %%
def get_gilead_fr():  # 受网速影响较大
    url = 'https://investors.gilead.com/financials/quarterly-results/default.aspx'
    chrome_options = webdriver.ChromeOptions()
    # #chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--log-level=3')
    # 实例化Chrome driver
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.get(url)
    browser.implicitly_wait(10)
    print('browser opened successfully!')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    div = soup.find_all('div', attrs={'class': 'module-financial-accordion_container js--active'})[0]
    year = div.h3.text
    div_quarter = div.find_all('div', attrs={'class': 'module_item'})[-1]
    quarter = div_quarter.find(name='h3').text.strip()
    output_dir = os.path.join('Gilead', year)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    hrefs_ = div_quarter.find_all(name='a')
    count = 0
    for h in hrefs_:
        href = h.get('href')
        if re.search('Press Release'.lower(), h.text.lower()):
            count += 1
            time.sleep(2)
            myfile = requests.get(href, allow_redirects=True)
            open(os.path.join(output_dir, 'Gilead {0} {1} {2}'.format(quarter, year, 'PR') + '.pdf'), 'wb').write(
                myfile.content)
        elif re.search('Earnings Presentation'.lower(), h.text.lower()):
            count += 1
            time.sleep(2)
            myfile = requests.get(href, allow_redirects=True)
            open(os.path.join(output_dir, 'Gilead {0} {1} {2}'.format(quarter, year, 'Presentation') + '.pdf'),
                 'wb').write(myfile.content)
        elif re.search('Supplementary Information'.lower(), h.text.lower()):
            count += 1
            time.sleep(2)
            myfile = requests.get(href, allow_redirects=True)
            open(os.path.join(output_dir, 'Gilead {0} {1} {2}'.format(quarter, year, 'Financials') + '.pdf'),
                 'wb').write(myfile.content)
        else:
            pass
    return year, quarter


# %%
if __name__ == '__main__':
    company_dict = {
        # Tier 2
        # 'EQRx':get_EQRx_fr, (no authentication)
        # 'Daiichi': get_Daiichi_fr,
        # 'GSK': get_GSK_fr,
        # 'JNJ': get_JNJ_fr,
        # 'Genmab':get_Genmab_fr,
        # 'Incyte':get_Incyte_fr,
        # 'Regeneron':get_Regeneron_fr,
        # 'Takeda':get_Takeda_fr,
        # 'HutchMed':get_HutchMed_fr,
        # 'junshi':get_junshi_fr,
        # 'Remegen':get_Remegen_fr,
        # 'Cstone':get_Cstone_fr,
        # 'Seagen':get_Seagen_fr(),
        # 'CSPC':get_CSPC_fr,
        # 'Hansoh':get_Hansoh_fr,
        # 'Sanofi':get_Sanofi_fr,
        # 'Gilead':get_gilead_fr,
    }

    company_time_dict = {}
    if os.path.exists('Tier2_Timestamp.log'):
        with open('Tier2_Timestamp.log', 'r') as t:
            json_dict = json.loads(t)
            company_time_dict = {x: datetime.strptime(y, '%Y/%m/%d') for x, y in json_dict.items()}

    with open('Tier2_FR.log', 'w') as f:
        for company in company_dict:
            f.write(company + '\n')
            try:
                if (company in company_time_dict.keys()) and (datetime.now() < company_time_dict[company]):
                    continue
                print('*' * 50)
                print('Now is checking for the latest update of {}'.format(company))
                year, quarter = company_dict[company]()
                next_run_time = datetime.now() + timedelta(days=40)

                if year and quarter:
                    f.write("Latest update for {0} is year {1} and quarter {2}\n".format(company, year, quarter))
                    f.write('\n')
                    f.flush()
                    company_time_dict[company] = next_run_time

                print('done for company {}'.format(company))

            except Exception as e:
                f.write('Update for company {0} failed due to error: {1}\n'.format(company, e))
                f.write('\n')
                f.flush()
                print('Error, The current company earnings report failed to download!')
                continue

        with open('Tier2_Timestamp.log', 'w') as timestamp:
            company_time_dict = {x: y.strftime('%Y/%m/%d') for x, y in company_time_dict.items()}
            timestamp.write(json.dumps(company_time_dict))
