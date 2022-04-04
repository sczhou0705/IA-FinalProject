import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import s3fs

def chrome(headless=False):
    # support to get response status and headers
    d = webdriver.DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'performance': 'ALL'}
    opt = webdriver.ChromeOptions()
    if headless:
        opt.add_argument("--headless")
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    opt.add_argument("--disable-popup-blocking")
    browser = webdriver.Chrome(executable_path=r'driver/chromedriver.exe', options=opt,desired_capabilities=d)
    browser.implicitly_wait(10)
    return browser

def main(event = None, context = None):
    print("Start running LinkedInScraper")
    ## Pass True if you want to hide chrome browser
    browser = chrome(True)
    browser.get('https://www.linkedin.com/uas/login')
    browser.implicitly_wait(3)
    file = open('config.txt')
    lines = file.readlines()
    username = lines[0]
    password = lines[1]


    elementID = browser.find_element_by_id('username')
    elementID.send_keys(username)

    elementID = browser.find_element_by_id('password')
    elementID.send_keys(password)

    elementID.submit()

    links = ['https://www.linkedin.com/in/atreish/',
            'https://www.linkedin.com/in/yuxiaoshen/',
            'https://www.linkedin.com/in/shichaoz/',
            'https://www.linkedin.com/in/mahlet-melese-1a509078/'
            ]
    values = []

    for link in links:
        browser.get(link)
        browser.implicitly_wait(1)
        def scroll_down_page(speed=8):
            current_scroll_position, new_height= 0, 1
            while current_scroll_position <= new_height:
                current_scroll_position += speed
                browser.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
                new_height = browser.execute_script("return document.body.scrollHeight")

        scroll_down_page(speed=8)

        src = browser.page_source
        soup = BeautifulSoup(src, 'lxml')
        # Get fullname
        try:
            name_div = soup.find('div', {'class': 'pv-text-details__left-panel'})
            first_last_name = name_div.find('h1').get_text().strip()
        except:
            first_last_name = None
        # Get location
        try:
            location_div = soup.find('div', {'class': 'pb2 pv-text-details__left-panel'})
            location = location_div.find('span').get_text().strip()
        except:
            location = None
        # Get experience
        li_tag = ""
        try:
            sections = soup.find_all('section')
            exp_section = ""
            for section in sections:
                exp_identifier = section.find('div', {'id':'experience'})
                if exp_identifier is not None:
                    exp_section = section
                    break
            div = exp_section.find('div', {'class':'pvs-list__outer-container'})
            ul = div.find('ul', {'class':'pvs-list'})
            li_tag = ul.find('li')
            #     print(li_tag)
        except:
            company_link = None
            title = None
            most_recent_company_name = None  
        try:
            company_link = li_tag.find('a', {'class':'optional-action-target-wrapper'})['href']
        except:
            company_link = None
        try:
            title = li_tag.find('span', {'class':'mr1'}).find('span').get_text().strip()
        except:
            title = None
        try:
            most_recent_company_name = li_tag.find('span', {'class':'t-14 t-normal'}).find('span').get_text().strip()
        except:
            most_recent_company_name = None
        values.append([first_last_name, location, most_recent_company_name, title, company_link])

    df = pd.DataFrame(values,columns = [["Full Name", "Location", "Most Recent Company", 'Job Title', 'Company Url']])
    ###LOAD THE FILE INTO S3####
    # prepare csv file name   
    pathname = 'ia-final-deployment/'#specify location of s3:/{my-bucket}/
    filenames = f"{pathname}linkedIn_info.csv" #name of the filepath and csv file

    #encoding must be adjusted to accommodate abnormal characters. Use s3fs to write to S3 bucket
    print("Start adding LinkedIn data to csv")
    byte_encoded_df = df.to_csv(None, index=False).encode() #encodes file as binary
    s3 = s3fs.S3FileSystem(anon=False)
    with s3.open(filenames, 'wb') as file:
        file.write(byte_encoded_df) #writes byte-encoded file to s3 location

    #print success message
    print("Successfull uploaded file to location:"+str(filenames))
    print("Complete running LinkedInScraper")