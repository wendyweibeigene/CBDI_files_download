# %%
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import os
import requests
import json
from datetime import datetime, timedelta
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
def get_abbvie_fr():
    url = 'https://investors.abbvie.com/financial-releases'
    res = requests.get(url=url)
    print('browser opened successfully!')
    soup = BeautifulSoup(res.text, 'lxml')
    reg = re.compile('AbbVie Reports.*Financial Results')
    table = soup.find('table', attrs={'class': 'nirtable news-table'})
    new_releases = table.tbody
    for news in new_releases.find_all('tr'):
        if re.findall(reg, news.text.strip().split('\n')[3]):
            h = news.find_all('td')[1].find(name='a').get('href')
            res = requests.get('https://investors.abbvie.com' + h)
            soup = BeautifulSoup(res.text, 'lxml')
            link_div = soup.find('div', attrs={'class': 'file-link'})
            year = link_div.text.strip().split(' ')[3]
            quarter = link_div.text.strip().split(' ')[2].split('-')[0]
            quarter = dicts[quarter.upper()]
            output_dir = os.path.join('Abbive', year)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            link = link_div.find(name='a').get('href')
            myfile = requests.get('https://investors.abbvie.com' + link, allow_redirects=True)
            open(
                os.path.join(output_dir, 'Abbive {0} {1} {2}'.format(year, quarter, 'Earnings Press Release') + '.pdf'),
                'wb').write(myfile.content)
            break
    return year, quarter


# %%
def get_agenus_fr():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    # EN
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    url = 'https://investor.agenusbio.com/financial-information/quarterly-results/default.aspx'
    browser.get(url)
    time.sleep(3)
    print('browser opened successfully!')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    table = soup.find('table', attrs={
        'summary': "Financial summary information documents organized year, quarter, and type. First column of each row under years organized by document type, press release, financial statement, earnings webcast, earnings presentation, earnings transcript, and annual reports"})
    # divs = soup.find('div',attrs={'class':'financial-list-year-content'})
    year = table.tr.th.text
    output_dir = os.path.join('Agenus', year)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    hrefs_ = table.tbody.tr.td.find_all('a')[::-1]

    for h in hrefs_:
        if h.get('aria-label'):
            quarter = h.span.text
            myfile = requests.get(h.get('href'), allow_redirects=True)
            open(os.path.join(output_dir, 'Agenus {0} {1} {2}'.format(quarter, year, 'PR') + '.pdf'), 'wb').write(
                myfile.content)
            time.sleep(3)
            break
    return year, quarter


# %%
def get_akeso_fr():
    dicts = {'Annual': 'FY', 'Interim': 'H1'}
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    # 实例化Chrome driver
    # EN
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    url = 'https://akesobio-umb.azurewebsites.net/en/investor-relations/financial-reports/'
    browser.get(url)
    time.sleep(3)
    print('browser opened successfully!')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    divs = soup.find('div', attrs={'class': 'financial-list-year-content'})
    year = divs.div.div.div.text.strip().split(' ')[0]
    output_dir = os.path.join('Akeso', year)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    quarter = divs.div.div.div.text.strip().split(' ')[1]
    quarter = dicts[quarter]
    hrefs_ = divs.div.div.div.find_all(name='a')
    h = hrefs_[0]
    myfile = requests.get('https://akesobio-umb.azurewebsites.net/' + h.get('href'), allow_redirects=True)
    open(os.path.join(output_dir, 'Akeso-{0} {1} {2}'.format(quarter, year, 'Results PR-EN') + '.pdf'), 'wb').write(
        myfile.content)
    time.sleep(3)
    # CN
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    url = 'https://akesobio.com/cn/investor-relations/financial-reports/'
    browser.get(url)
    time.sleep(3)
    # print('browser opened successfully!')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    divs = soup.find('div', attrs={'class': 'financial-list-year-content'})
    hrefs_ = divs.div.div.div.find_all(name='a')
    h = hrefs_[0]
    myfile = requests.get('https://akesobio.com/' + h.get('href'), allow_redirects=True)
    open(os.path.join(output_dir, 'Akeso-{0} {1} {2}'.format(quarter, year, 'Results PR-CN') + '.pdf'), 'wb').write(
        myfile.content)
    time.sleep(3)
    # presentation
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    url = 'https://akesobio.com/cn/investor-relations/presentations/'
    browser.get(url)
    time.sleep(3)
    # print('browser opened successfully!')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    divs = soup.find('div', attrs={'class': 'presentations-list-year-content'})
    hrefs_ = divs.div.div.find_all(name='a')
    h = hrefs_[0]
    myfile = requests.get('https://akesobio.com/' + h.get('href'), allow_redirects=True)
    open(os.path.join(output_dir, 'Akeso-{0} {1} {2}'.format(quarter, year, 'Results Presentation-CN') + '.pdf'),
         'wb').write(myfile.content)
    return year, quarter


# %%
def get_Amgen_fr():
    url = r'https://investors.amgen.com/financials/quarterly-earnings'
    res = requests.get(url=url)
    soup = BeautifulSoup(res.text, 'lxml')
    reg_1 = re.compile('.FINANCIAL RESULTS*')
    reg_2 = re.compile('.Earnings Presentation*')
    div_tags = soup.find_all('div', attrs={'class': 'view-grouping'})
    for div_tag in div_tags:
        hrefs_ = div_tag.find_all(name='a')
        if len(hrefs_) > 1:
            c = div_tag.contents[1].string
            year = c.strip().split(' ')[1]
            quarter = c.strip().split(' ')[0]
            output_dir = os.path.join('Amgen', year)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            count = 0
            hrefs_ = div_tag.find_all(name='a')
            for h in hrefs_:
                if re.search(reg_1, h.string):
                    count += 1
                    href = h.get('href')
                    soup2 = BeautifulSoup(requests.get(url='https://investors.amgen.com/' + href).text, 'lxml')
                    file_link = 'https://investors.amgen.com' + soup2.find('div', attrs={'class': 'file-link'}).find(
                        name='a').get('href')
                    myfile = requests.get(file_link, allow_redirects=True)
                    open(os.path.join(output_dir,
                                      'Amgen {0} {1} {2}'.format(quarter, year, 'Earnings Press Release') + '.pdf'),
                         'wb').write(myfile.content)
                    # print('Downloaded {0} for Amgen'.format(count))
                if re.search(reg_2, h.string):
                    count += 1
                    file_link = 'https://investors.amgen.com' + h.get('href')
                    myfile = requests.get(file_link, allow_redirects=True)
                    open(os.path.join(output_dir,
                                      'Amgen {0} {1} {2}'.format(quarter, year, 'Earnings Presentation') + '.pdf'),
                         'wb').write(myfile.content)

            break
        else:
            pass
    return year, quarter


# %%
def get_bms_fr():
    url = 'https://www.bms.com/investors/events-and-presentations.html'
    # url = 'https://bristolmyers2016ir.q4web.com/feed/Event.svc/GetEventList?eventDateFilter=0&amp;languageId=1&amp;sortOperator=1'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('-ignore-certificate-errors')
    chrome_options.add_argument('-ignore -ssl-errors')
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--log-level=3')
    # 实例化Chrome driver
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.get(url)
    browser.implicitly_wait(10)
    browser.find_element(By.ID, "onetrust-accept-btn-handler").click()
    browser.find_element(By.ID, "investor_evenets--presentations_past").click()
    browser.implicitly_wait(10)
    s = browser.find_element(By.ID, 'events_yearslist')
    s1 = Select(s)
    time.sleep(5)
    s1.select_by_value(s1.options[0].text)
    print('browser opened successfully!')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    div = soup.find('div', attrs={'class': 'investor_events--presentations-past'})
    year = s1.options[0].text

    reg_1 = re.compile('Bristol Myers Squibb.*Results Conference Call')
    for div_tag in div.find_all('div', attrs={'class': 'investor-event'}):
        cur_div = div_tag.find('div', attrs={'class': 'event-title'})
        count = 0
        c = cur_div.text.strip()
        if re.findall(reg_1, c):
            year = c.split(' ')[4]
            quarter = c.split(' ')[3]
            output_dir = os.path.join('BMS', year)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            hrefs_ = div_tag.find_all(name='a')
            for h in hrefs_:
                href = h.get('href')
                if re.search('Press Release'.lower(), h.text.lower()):
                    count += 1
                    time.sleep(2)
                    myfile = requests.get(href, allow_redirects=True)
                    open(os.path.join(output_dir, 'BMS {0} {1} {2}'.format(quarter, year, 'Press Release') + '.pdf'),
                         'wb').write(myfile.content)
                elif re.search('Results Presentation \(with Appendix\)'.lower(), h.text.lower()):
                    count += 1
                    time.sleep(2)
                    myfile = requests.get(href, allow_redirects=True)
                    open(os.path.join(output_dir, 'BMS {0} {1} {2}'.format(quarter, year, 'Presentation') + '.pdf'),
                         'wb').write(myfile.content)
                elif href.split('.')[-1] == 'xlsx':
                    count += 1
                    time.sleep(2)
                    myfile = requests.get(href, allow_redirects=True)
                    open(os.path.join(output_dir, 'BMS {0} {1} {2}'.format(quarter, year, 'Financials') + '.xlsx'),
                         'wb').write(myfile.content)
                else:
                    pass
            # print('Downloaded {0} for BMS'.format(count))
            break
    if not quarter:
        return 'No FR for year {}'.format(year), None
    else:
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
def get_AstraZeneca_fr():
    url = 'https://www.astrazeneca.com/investor-relations/events.html'
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
    # browser.find_element(By.XPATH, '//*[@id="CookieReportsBannerAZ"]/div[1]/div[3]/a[1]').click()

    browser.find_element(By.XPATH, '//*[@id="main"]/div/div[3]/div/div/div/div/div/div[2]/div[2]/button').click()

    soup = BeautifulSoup(browser.page_source, 'lxml')

    # soup= BeautifulSoup(res.text,'lxml')
    div = soup.find('div', attrs={
        'class': 'events-listing__block-wrapper events-listing__block-wrapper--past js-events-listing__block-wrapper--past'})
    divs = div.find_all('div', attrs={'class': 'event-card js-event-card'})

    for idx, div_tag in enumerate(divs):
        if div_tag.a:
            text = div_tag.a.text.strip()
            if re.findall(re.compile('\d+ results'), text):
                temp = re.split(r' ', text)
                year = temp[-2]
                quarter = temp[-3]
                link = 'https://www.astrazeneca.com/content/astraz' + div_tag.a.get('href')
                break
    output_dir = os.path.join('AstraZeneca', year)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    try:
        browser.get(link)
        browser.implicitly_wait(5)
    except Exception:
        browser.execute_script('window.stop()')

    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    for div_tag in soup.find_all('div', attrs={'class': 'download__item section'}):
        if re.findall(re.compile('{0} {1} results announcement'.format(quarter, year)), div_tag.text.strip()):
            h = div_tag.find_all(name='a')[0]
            myfile = requests.get('https://www.astrazeneca.com' + h.get('href'), allow_redirects=True,
                                  headers=myheaders)
            open(os.path.join(output_dir, 'AZ {0} {1} {2}'.format(quarter, year, 'Press Release') + '.pdf'),
                 'wb').write(myfile.content)
        elif re.findall(re.compile('{0} {1} results presentation'.format(quarter, year)), div_tag.text.strip()):
            h = div_tag.find_all(name='a')[0]
            myfile = requests.get('https://www.astrazeneca.com' + h.get('href'), allow_redirects=True,
                                  headers=myheaders)
            open(os.path.join(output_dir, 'AZ {0} {1} {2}'.format(quarter, year, 'Presentation') + '.pdf'), 'wb').write(
                myfile.content)
        elif re.findall(re.compile('{0} {1} results clinical trials appendix'.format(quarter, year)),
                        div_tag.text.strip()):
            h = div_tag.find_all(name='a')[0]
            myfile = requests.get('https://www.astrazeneca.com' + h.get('href'), allow_redirects=True,
                                  headers=myheaders)
            open(os.path.join(output_dir, 'AZ {0} {1} {2}'.format(quarter, year, 'Trials Appendix') + '.pdf'),
                 'wb').write(myfile.content)
        else:
            pass
    return year, quarter


# %%
def get_merck_fr():
    url = "https://www.merck.com/investor-relations/events-and-presentations/"
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--log-level=3')
    # 实例化Chrome driver
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.get(url)
    time.sleep(3)
    print('browser opened successfully!')
    browser.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
    browser.find_element(By.XPATH, '//*[@id="fowardGuidanceModel"]/div/div/div[2]/a[2]').click()
    browser.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/div[1]/button[3]').click()
    s = browser.find_element(By.XPATH,
                             '//*[@id="mco-q4-events-list-block-block_58a506205abf6821eae173c235a6b6ef"]/div[1]/div[2]/div/select')
    s1 = Select(s)
    time.sleep(5)
    # s1.select_by_value(s1.options[0].text)
    year = s1.options[0].text
    quarter = None
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    div = soup.find('div', attrs={'class': 'mco-q4-events-list-block-events-item-list-container'})
    for div_tag in div.find_all('div', attrs={'class': 'mco-q4-events-list-block-events-item-container'}):
        title = div_tag.find_all('p')[2].text
        if re.search('Earnings Call', title.strip()):
            year = title.strip().split(' ')[-3]
            quarter = title.strip().split(' ')[-4]
            output_dir = os.path.join('Merck', year)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            hrefs_ = div_tag.find('div', attrs={'mco-q4-events-list-events-item-link-containers'}).find_all(name='a')
            for h in hrefs_:
                href = h.get('href')
                if re.search('Financial Disclosures', h.text.strip()) and href.split('.')[-1] == 'pdf':
                    time.sleep(2)
                    myfile = requests.get(href, allow_redirects=True)
                    open(os.path.join(output_dir, 'Merck {0} {1} {2}'.format(quarter, year, 'Financials') + '.pdf'),
                         'wb').write(myfile.content)
                elif re.search('Earnings Presentation', h.text.strip()) and href.split('.')[-1] == 'pdf':
                    time.sleep(2)
                    myfile = requests.get(href, allow_redirects=True)
                    open(os.path.join(output_dir, 'Merck {0} {1} {2}'.format(quarter, year, 'Presentation') + '.pdf'),
                         'wb').write(myfile.content)
                elif re.search('Earnings Announcement', h.text.strip()) and href.split('.')[-1] == 'pdf':
                    time.sleep(2)
                    myfile = requests.get(href, allow_redirects=True)
                    open(os.path.join(output_dir, 'Merck {0} {1} {2}'.format(quarter, year, 'PR') + '.pdf'),
                         'wb').write(myfile.content)
            break
    if not quarter:
        return 'No FR for year {}'.format(year), quarter
    else:
        return year, quarter


# %%
def get_Novartis_fr():
    url = 'https://www.novartis.com/investors/financial-data/quarterly-results'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                               options=chrome_options)  # chrome_options=chrome_options
    browser.get(url)
    time.sleep(3)
    print('browser opened successfully!')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    div = soup.find('div', attrs={
        'class': 'clearfix text-formatted field field--name-field-tab-body-text-content field--type-text-long field--label-hidden field__item'})
    year = div.h2.text.strip().split(' ')[1]
    quarter = div.h2.text.strip().split(' ')[0]
    output_dir = os.path.join('Novartis', year)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    hrefs_ = div.find_all(name='a')
    count = 0
    for h in hrefs_:
        if re.search('financial report', h.text.strip()):
            count += 1
            myfile = requests.get('https://www.novartis.com/' + h.get('href'), allow_redirects=True)
            open(os.path.join(output_dir, 'Novartis {0} {1} {2}'.format(quarter, year, 'Financial Report') + '.pdf'),
                 'wb').write(myfile.content)
        elif re.search('English', h.text.strip()):
            count += 1
            myfile = requests.get('https://www.novartis.com/' + h.get('href'), allow_redirects=True)
            open(os.path.join(output_dir, 'Novartis {0} {1} {2}'.format(quarter, year, 'PR') + '.pdf'), 'wb').write(
                myfile.content)
        if re.search('presentation', h.text.strip()):
            count += 1
            myfile = requests.get('https://www.novartis.com/' + h.get('href'), allow_redirects=True)
            open(os.path.join(output_dir, 'Novartis {0} {1} {2}'.format(quarter, year, 'Presentation') + '.pdf'),
                 'wb').write(myfile.content)

    return year, quarter


# %%
def get_InnoCare_fr():  ## 中期和年度汇报有PDF， 第一季度和第三季度只有视频回放
    # dicts = {'第一季度':'Q1','中期':'1H','第三季度':'Q3','全年':'FY'}
    # # presentation
    # url = 'https://cn.innocarepharma.com/investor/materia'
    # chrome_options = webdriver.ChromeOptions()
    # #chrome_options.add_argument('--headless')
    # # chrome_options.add_argument('--start-maximized')
    # browser=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    # browser.set_window_size(1180,960)
    # browser.set_page_load_timeout(50)
    # try:
    #     browser.get(url)
    #     browser.implicitly_wait(5)
    # except Exception:
    #     browser.execute_script('window.stop()')
    # print('browser opened successfully!')
    # browser.implicitly_wait(5)
    # browser.find_element_by_xpath('//*[@id="cookieNotice"]/div/div/div/div[2]/uni-view[2]').click()
    # # for i in range(1,10):
    # i= 1
    # element_title = browser.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view/uni-view[4]/uni-view[2]/uni-view[1]/uni-view[2]')
    # title = element_title.text
    # if re.search('业绩演示材料',title.strip()):
    #     year = title[:4]
    #     for key in dicts:
    #         if key in title:
    #             quarter = dicts[key]
    #     output_dir = os.path.join('InnoCare',year)
    #     if not os.path.exists(output_dir):
    #         os.makedirs(output_dir)
    # browser.execute_script('window.scrollBy(0,700)')
    # browser.implicitly_wait(5)
    # # if year:
    # browser.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view/uni-view[4]/uni-view[2]/uni-view[1]/uni-view[3]/uni-view').click()
    # handles = browser.window_handles
    # browser.switch_to.window(handles[1])
    # url = browser.current_url
    # myfile = requests.get(url,allow_redirects=True)
    # open(os.path.join(output_dir,'Innocare {0} {1} {2}'.format(quarter, year, 'Results - Presentation CN')+'.pdf'),'wb').write(myfile.content)
    # browser.quit()
    # PR
    url = 'https://www.innocarepharma.com/investor/circular'
    dicts = {'中期': '1H', '年度': 'FY', '第三季度': 'Q3', '第一季度': 'Q1', '第二季度': 'Q2'}
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.set_window_size(1180, 960)
    browser.set_page_load_timeout(50)
    try:
        browser.get(url)
        browser.implicitly_wait(5)
    except Exception:
        browser.execute_script('window.stop()')
    print('browser opened successfully!')
    browser.find_element_by_xpath('//*[@id="cookieNotice"]/div/div/div/div[2]/uni-view[2]').click()
    browser.execute_script('window.scrollBy(0,1000)')
    browser.switch_to.default_content()
    frame = browser.find_elements(By.TAG_NAME, 'iframe')[0]
    browser.switch_to.frame(frame)
    pages = browser.find_element(By.XPATH, '//*[@id="PagesContainer"]/table/tbody/tr/td[2]')
    if 1:
        soup = BeautifulSoup(browser.page_source, 'lxml')
        divs = soup.find_all('div', attrs={'class': re.compile('PressRelease PressRelease*')})
        for div in divs:
            title = div.find('div', attrs={
                'class': 'NewsColumn-Container PressRelease-NewsColumn PressRelease-SingleLine-DataRow'}).text.strip()
            if re.findall(re.compile('诺诚健华医药.*报告|港股公告.*业绩公告'), title):
                year = re.findall('\d\d\d\d', title)[0]
                for key in dicts:
                    if re.search(key, title):
                        quarter = dicts[key]
                output_dir = os.path.join('InnoCare', year)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                stop = True
                link = div.find_all(name='a')[0].get('href')
                soup_n = BeautifulSoup(requests.get('https://asia.tools.euroland.com' + link).text)
                h = soup_n.find('div', attrs={'id': 'SeparateNews-Body'}).find('a')
                myfile = requests.get(h.get('href'), allow_redirects=True)
                open(os.path.join(output_dir, 'Innocare {0} {1} {2}'.format(quarter, year, 'Results -PR EN') + '.pdf'),
                     'wb').write(myfile.content)
                break
            else:
                stop = False
                continue
                # pass
    if not stop:
        for i in range(1, len(pages.text)):
            xpath = '//*[@id="PagesContainer"]/table/tbody/tr/td[2]/a[{0}]'.format(i)
            browser.find_element_by_xpath(xpath).click()
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, 'lxml')
            divs = soup.find_all('div', attrs={'class': re.compile('PressRelease PressRelease*')})
            for div in divs:
                title = div.find('div', attrs={
                    'class': 'NewsColumn-Container PressRelease-NewsColumn PressRelease-SingleLine-DataRow'}).text.strip()
                if re.findall(re.compile('诺诚健华医药.*报告|港股公告.*业绩公告'), title):
                    year = re.findall('\d\d\d\d', div.text)[0]
                    for key in dicts:
                        if re.search(key, title):
                            quarter = dicts[key]
                    output_dir = os.path.join('InnoCare', year)
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    link = div.find_all(name='a')[0].get('href')
                    soup_n = BeautifulSoup(requests.get('https://asia.tools.euroland.com' + link).text)
                    h = soup_n.find('div', attrs={'id': 'SeparateNews-Body'}).find('a')
                    myfile = requests.get(h.get('href'), allow_redirects=True)
                    open(os.path.join(output_dir,
                                      'Innocare {0} {1} {2}'.format(quarter, year, 'Results -PR EN') + '.pdf'),
                         'wb').write(myfile.content)
                    break
            else:
                continue
            break
    browser.quit()
    # report
    url = 'https://cn.innocarepharma.com/investor/reporting'
    dicts = {'第一季度': 'Q1', '中期': '1H', '第三季度': 'Q3', '年度': 'FY'}
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.get(url)
    time.sleep(3)
    print('browser opened successfully!')
    browser.find_element_by_xpath('//*[@id="cookieNotice"]/div/div/div/div[2]/uni-view[2]').click()
    soup = BeautifulSoup(browser.page_source, 'lxml')
    title = browser.find_element_by_xpath(
        '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view/uni-view[5]/uni-view[1]/uni-view[2]/uni-view[1]').text
    year = re.findall('\d\d\d\d', title)[0]
    for key in dicts:
        if re.search(key, title):
            quarter = dicts[key]
    browser.find_element_by_xpath(
        '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view/uni-view[5]/uni-view[1]/uni-view[2]/uni-view[3]/uni-view/uni-view[2]').click()
    handles = browser.window_handles
    browser.switch_to.window(handles[1])
    url = browser.current_url
    myfile = requests.get(url, allow_redirects=True)
    open(os.path.join(output_dir, 'Innocare {0} {1} {2}'.format(quarter, year, 'Report - CN') + '.pdf'), 'wb').write(
        myfile.content)
    browser.quit()
    return year, quarter


# %%
def get_Innovent_fr():
    # presentation
    dicts = {'annual': 'FY', 'interim': 'H1'}
    url = 'https://www.innoventbio.com/InvestorsAndMedia/WebcastsAndPresentations'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.set_window_size(1180, 960)
    browser.set_page_load_timeout(50)
    try:
        browser.get(url)
        browser.implicitly_wait(5)
    except Exception:
        browser.execute_script('window.stop()')
    print('browser opened successfully!')
    browser.execute_script('window.scrollBy(0,500)')
    # browser.switch_to.default_content()
    # frame = browser.find_elements_by_tag_name('iframe')[0]  
    # browser.switch_to.frame(frame) 
    # browser.implicitly_wait(5)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    divs = soup.find_all('div', attrs={'class': 'row fileList'})
    browser.quit()
    for ppt in divs:
        if re.search('innovent biologics.*results(_)?main file', ppt.a.text.strip().lower()):
            year = re.findall('\d\d\d\d', ppt.a.text.strip().lower())[0]
            for key in dicts:
                if re.search(key, ppt.a.text.strip().lower()):
                    quarter = dicts[key]
            output_dir = os.path.join('Innovent', year)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            h = ppt.find('a').get('href')
            myfile = requests.get(h, allow_redirects=True)
            open(os.path.join(output_dir, 'Innovent-{0} {1} {2}'.format(quarter, year, 'Presentation - EN') + '.pdf'),
                 'wb').write(myfile.content)
            break
    # report
    url = 'https://www.innoventbio.com/InvestorsAndMedia/InformationDisclosure/AnnouncementsAndCirculars'
    dicts = {'annual': 'FY', 'interim': 'H1'}
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.get(url)
    browser.implicitly_wait(5)
    browser.execute_script('window.scrollBy(0,1000)')
    browser.switch_to.default_content()
    frame = browser.find_elements(By.TAG_NAME, 'iframe')[0]
    browser.switch_to.frame(frame)
    browser.implicitly_wait(5)
    pages = browser.find_element(By.XPATH, '//*[@id="PagesContainer"]/table/tbody/tr/td[2]')
    if 1:
        soup = BeautifulSoup(browser.page_source, 'lxml')
        divs = soup.find_all('div', attrs={'class': re.compile('PressRelease PressRelease*')})
        for div in divs:
            title = div.find('div', attrs={
                'class': 'NewsColumn-Container PressRelease-NewsColumn PressRelease-SingleLine-DataRow'}).text.strip()
            if re.findall(re.compile('.*RESULTS ANNOUNCEMENT.*'), title):
                year = re.findall('\d\d\d\d', title)[0]
                for key in dicts:
                    if re.search(key, title.lower()):
                        quarter = dicts[key]
                    output_dir = os.path.join('Innovent', year)
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    stop = True
                    link = div.find_all(name='a')[0].get('href')
                    soup_n = BeautifulSoup(requests.get('https://asia.tools.euroland.com' + link).text)
                    h = soup_n.find('div', attrs={'id': 'SeparateNews-Body'}).find('a')
                    myfile = requests.get(h.get('href'), allow_redirects=True)
                    open(os.path.join(output_dir, 'Innovent-{0} {1} {2}'.format(quarter, year, 'Report-EN') + '.pdf'),
                         'wb').write(myfile.content)
                    break
            else:
                stop = False
                continue
                # pass
    if not stop and len(pages.text):
        for i in range(1, len(pages.text)):
            xpath = '//*[@id="PagesContainer"]/table/tbody/tr/td[2]/a[{0}]'.format(i)
            browser.find_element_by_xpath(xpath).click()
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, 'lxml')
            divs = soup.find_all('div', attrs={'class': re.compile('PressRelease PressRelease*')})
            for div in divs:
                title = div.find('div', attrs={
                    'class': 'NewsColumn-Container PressRelease-NewsColumn PressRelease-SingleLine-DataRow'}).text.strip()
                if re.findall(re.cmpile('.*RESULTS ANNOUNCEMENT.*'), title):
                    year = re.findall('\d\d\d\d', title)[0]
                    for key in dicts:
                        if re.search(key, title.lower()):
                            quarter = dicts[key]
                        output_dir = os.path.join('Innovent', year)
                        if not os.path.exists(output_dir):
                            os.makedirs(output_dir)
                        stop = True
                        link = div.find_all(name='a')[0].get('href')
                        soup_n = BeautifulSoup(requests.get('https://asia.tools.euroland.com' + link).text)
                        h = soup_n.find('div', attrs={'id': 'SeparateNews-Body'}).find('a')
                        myfile = requests.get(h.get('href'), allow_redirects=True)
                        open(os.path.join(output_dir,
                                          'Innovent-{0} {1} {2}'.format(quarter, year, 'Report-EN') + '.pdf'),
                             'wb').write(myfile.content)
                        break
                else:
                    continue
                break
    browser.quit()
    # report CN
    url = 'https://investor.innoventbio.com/cn/investors/information-disclosure/financial-reports/'
    dicts = {'年度': 'FY', '中期': 'H1'}
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.get(url)
    browser.implicitly_wait(5)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    div = soup.find('div', attrs={'class': 'second-block'})
    title = div.text.strip()
    year = re.findall('\d\d\d\d', title)[0]
    for key in dicts:
        if re.search(key, title.lower()):
            quarter = dicts[key]
    output_dir = os.path.join('Innovent', year)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    h = div.find(name='a').get('href')
    myfile = requests.get('https://investor.innoventbio.com/' + h, allow_redirects=True)
    open(os.path.join(output_dir, 'Innovent-{0} {1} {2}'.format(quarter, year, 'Report- CN') + '.pdf'), 'wb').write(
        myfile.content)
    return year, quarter


# %%
def get_ZaiLab_fr():
    # PR_EN
    url = 'https://ir.zailaboratory.com/news-media/press-releases?a89c091f_items_per_page=10&a89c091f_year%5Bvalue%5D=_none&op=Filter&a89c091f_widget_id=a89c091f&form_build_id=form-eIiLrpkZmQ66-4dtvYImRJ3_WtgxYxxNbvzxibUypzA&form_id=widget_form_base'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.get(url)
    browser.implicitly_wait(5)
    # s = browser.find_element(By.ID,'edit_a89c091f_year_value_chosen')
    # s1 = Select(s)
    # time.sleep(5)
    # s1.select_by_value(s1.options[0].text)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    # browser.quit()
    divs = soup.find_all('div', attrs={'class': re.compile('col-md-6')})
    dicts = {'FIRST': 'Q1', 'SECOND': 'Q2', 'THIRD': 'Q3', 'FULL-YEAR': 'Q4'}
    for div in divs:
        title = div.p.text.strip()
        if re.search(re.compile('Zai Lab Announces.*Financial Results'.lower()), title.lower()):
            year = re.findall('\d\d\d\d', title)[0]
            for key in dicts:
                if re.search(key.lower(), title.lower()):
                    quarter = dicts[key]
            output_dir = os.path.join('Zai lab', year)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            link = div.find('a').get('href')
            break
    if link:
        soup_n = BeautifulSoup(requests.get('https://ir.zailaboratory.com/' + link).text)
        h = soup_n.find('div', attrs={'class': 'file-link pdf-file-link'}).find('a')
        myfile = requests.get('https://ir.zailaboratory.com/' + h.get('href'), allow_redirects=True)
        open(os.path.join(output_dir, "Zai Lab {0}'{1} {2}".format(quarter, year[-2:], 'Results-PR EN') + '.pdf'),
             'wb').write(myfile.content)

    # PR-CN
    url = 'https://ir.zailaboratory.com/zh-hans/news-media/press-releases'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.get(url)
    browser.implicitly_wait(5)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    divs = soup.find_all('div', attrs={'class': re.compile('col-md-6')})
    dicts = {'第一季度': 'Q1', '第二季度': 'Q2', '第三季度': 'Q3', '全年': 'Q4'}
    for div in divs:
        title = div.p.text.strip()
        if re.search(re.compile('再鼎医药公布.*财务业绩'.lower()), title.lower()):
            year = re.findall('\d\d\d\d', title)[0]
            for key in dicts:
                if re.search(key.lower(), title.lower()):
                    quarter = dicts[key]
            output_dir = os.path.join('Zai lab', year)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            link = div.find('a').get('href')
            break
    if link:
        soup_n = BeautifulSoup(requests.get('https://ir.zailaboratory.com/' + link).text)
        h = soup_n.find('div', attrs={'class': 'file-link pdf-file-link'}).find('a')
        myfile = requests.get('https://ir.zailaboratory.com/' + h.get('href'), allow_redirects=True)
        open(os.path.join(output_dir, "Zai Lab {0}'{1} {2}".format(quarter, year[-2:], 'Results-PR CN') + '.pdf'),
             'wb').write(myfile.content)
    # presentation
    url = 'https://ir.zailaboratory.com/webcasts-presentations'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.get(url)
    browser.implicitly_wait(5)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    div = soup.find('div', attrs={'class': re.compile('block--asset-presentations.*')})
    h = div.find('div', attrs={'class': 'nir-widget--list'}).div.find('a')
    myfile = requests.get('https://ir.zailaboratory.com/' + h.get('href'), allow_redirects=True)
    open(os.path.join(output_dir, "Zai Lab {0}'{1} {2}".format(quarter, year[-2:], 'Presentation EN') + '.pdf'),
         'wb').write(myfile.content)
    return year, quarter


def get_UCB_fr():
    url = 'https://www.ucb.com/investors/download-center'
    res = requests.get(url, headers=myheaders)
    time.sleep(3)
    print('browser opened successfully!')
    soup = BeautifulSoup(res.text, 'lxml')
    count = 0
    div = soup.find_all('div', attrs={'class': 'columns small-12 medium-4'})
    for div_tag in div:
        if div_tag.h2:
            if re.match(re.compile('\d+.*Results'), div_tag.h2.text.strip()):
                year = div_tag.h2.text.strip().split(' ')[0]
                quarter = div_tag.h2.text.strip().split(' ')[1]
                sections = div_tag.find_all('section')
                break
    output_dir = os.path.join('UCB', year)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if sections:
        for section in sections:
            if re.search('Management Report'.lower(), section.text.strip().lower()):
                h = section.find_all('a')[0]
                myfile = requests.get(h.get('href'), allow_redirects=True)
                open(os.path.join(output_dir, "UCB {0} {1} {2}".format(quarter, year, 'Report-EN') + '.pdf'),
                     'wb').write(myfile.content)
            elif re.search('Presentation'.lower(), section.text.strip().lower()):
                h = section.find_all('a')[0]
                myfile = requests.get(h.get('href'), allow_redirects=True)
                open(os.path.join(output_dir, "UCB {0} {1} {2}".format(quarter, year, 'Presentaion') + '.pdf'),
                     'wb').write(myfile.content)
            else:
                continue
    return year, quarter


# %%
if __name__ == '__main__':
    company_dict = {
        ### Tier 1
        # 'Akeso': get_akeso_fr,
        # 'Abbvie': get_abbvie_fr,
        # 'Agenus': get_agenus_fr,
        # 'Amgen': get_Amgen_fr,
        # 'BMS': get_bms_fr,
        # 'Gilead': get_gilead_fr,
        'Novartis': get_Novartis_fr,
        # 'AstraZeneca': get_AstraZeneca_fr,
        # 'Merck': get_merck_fr,
        # 'Innovent': get_Innovent_fr,
        # 'Zai Lab': get_ZaiLab_fr,
        # 'UCB': get_UCB_fr,
    }

    company_time_dict = {}
    if os.path.exists('Tier1_Timestamp.log'):
        with open('Tier1_Timestamp.log', 'r') as t:
            json_dict = json.loads(t)
            company_time_dict = {x: datetime.strptime(y, '%Y/%m/%d') for x, y in json_dict.items()}

    with open('Tier1_FR.log', 'a+') as f:
        for company in company_dict:
            f.write(company + '\n')
            try:
                if company in company_time_dict.keys() and datetime.now() < company_time_dict[company]:
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

        with open('Tier1_Timestamp.log', 'w') as timestamp:
            company_time_dict = {x: y.strftime('%Y/%m/%d') for x, y in company_time_dict.items()}
            timestamp.write(json.dumps(company_time_dict))

