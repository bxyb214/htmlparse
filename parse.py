#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

BASE_URL = 'http://10.0.5.208/prpall'
BASE_SUB_URL = '/{kind}/tbcbpg/UIPrPoEn{kind}Show.jsp?BIZTYPE=POLICY&BizNo=110{region}{kind}{year}{number}YD&SHOWTYPE=SHOW&RiskCode={kind}'

KINDS = ["0507", "0508"]                          #险种
REGIONS = ["01", "02", "03"]
YEARS = ["2015", "2016"]
NUMBERS = range(1, 999999)
PAGE_404 = 'Error 404--Not Found'
PAGE_ERROR = '信息反馈'

def process():
    driver = webdriver.Chrome()
    flag = 0
    count = 0
    for kind in KINDS:
        for region in REGIONS:
            for year in YEARS:
                for number in NUMBERS:
                    if count > 100:
                        print ("count>100")
                        return
                    print ("count = " + str(count))
                    time.sleep(1)
                    url = BASE_URL + BASE_SUB_URL.replace("{kind}", kind).replace("{region}", region).replace("{year}", year).replace("{number}", str(number).zfill(6))
                    print (url)
                    driver.get(url)
                    WebDriverWait(driver,10)
                    html_source = driver.page_source
                    if PAGE_404 in html_source or PAGE_ERROR in html_source:
                        flag += 1
                        break
                    else:
                        flag = 0
                        search_box = driver.find_element_by_name('ProposalNo')
                        # print (search_box.source)
                        ProposalNo =  search_box.get_attribute('value')
                        outfile = open('example.csv', 'a')
                        writer = csv.writer(outfile)
                        writer.writerow([ProposalNo, url])
                        outfile.close()
                    count += 1
                    if flag > 0:
                        print (">0")
                        break
                if flag > 1:
                    print (">1")
                    break
            if flag > 2:
                print (">2")
                break

def process_single():

    kind = "0507"
    region = "01"
    year = "2016"
    number = 1
    driver = webdriver.Chrome()
    url = BASE_URL + BASE_SUB_URL.replace("{kind}", kind).replace("{region}", region).replace("{year}", year).replace("{number}", str(number).zfill(6))
    print (url)
    driver.get(url)
    WebDriverWait(driver,10)
    html_source = driver.page_source
    if PAGE_404 in html_source:
        print ("404")
    else:
        search_box = driver.find_element_by_name('ProposalNo')
        # print (search_box.source)
        CIPolicyNo =  search_box.get_attribute('value')
        print (CIPolicyNo)
        output_file = csv.writer(open('output.csv', 'w'), delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        output_file.writerow(CIPolicyNo, url)
        # output_file.close()
    # driver.quit()

def csv_write():
    CIPolicyNo = "11"
    url = "2"
    outfile = open('example.csv', 'a')
    writer = csv.writer(outfile)
    writer.writerow([CIPolicyNo, url])
    outfile.close()

if __name__ == '__main__':
    # process_single()
    process()
    # csv_write()
