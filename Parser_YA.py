from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime
import xlrd
import re
import os


def read_file(data_file_name):
    azs_dir = []
    excel_data_file = xlrd.open_workbook(data_file_name)
    sheet = excel_data_file.sheet_by_index(0)
    for i in range(1, sheet.nrows):
        st_id = str(sheet.row(i)[0])[7:-2]
        st_url = str(sheet.row(i)[4])[6:-1]
        if len(st_url) > 5:
            azs_data = {'ID': st_id, 'link': st_url}
            azs_dir.append(azs_data)
    return azs_dir


def get_prices(url):
    azs_prices = {}
    browser = webdriver.Firefox()
    browser.get(url)
    time.sleep(0.5)
    buttons = browser.find_elements_by_class_name('card-dropdown-view__control')
    for button in buttons:
        try:
            button.click()
        except:
            print('some buttons failed')
    try:
        fuel_names_block = browser.find_elements_by_class_name('search-fuel-info-view__name')
        prices_block = browser.find_elements_by_class_name('search-fuel-info-view__value')
    except NoSuchElementException:
        print('No data')
        fuel_names_block = prices_block = []
    try:
        comment = browser.find_element_by_class_name('search-fuel-info-view__info')
    except NoSuchElementException:
        print('No comment')
    for i in range(len(fuel_names_block)):
        fuel_name = fuel_names_block[i].text
        fuel_price = re.sub(',', '.', prices_block[i].text)
        if fuel_price == '–':
            fuel_price = ''
        azs_prices[fuel_name] = fuel_price + ',' + comment.text
    browser.close()
    return azs_prices


def form_strings(azs_prices, ID):
    csv_data = ''
    for fuel_name in azs_prices.keys():
        parse_date = datetime.now().strftime("%Y-%m-%d,%H:%M:%S")
        csv_data += ID+ ',' + ',' + fuel_name + ',' + azs_prices[fuel_name] + ',' + ',' + parse_date + ',' + 'YA_maps\n'
    print(csv_data)
    return csv_data


if not os.path.exists('parsed_prices'):
    os.mkdir(r'parsed_prices')
file_w_name = datetime.today().strftime('%Y-%m-%d') + '_YA_maps.csv'

Data_file_name = r'C:\Users\GPN-Centre\Desktop\parsing\Data.xlsx'
azs_list = read_file(Data_file_name)
file_w = open(file_w_name, 'a')

for azs in azs_list:
    ID = azs['ID']
    azs_price = get_prices(azs['link'])
    csv_data = form_strings(azs_price, ID)
    file_w.write(csv_data)
file_w.close()

#file check:
fr = open(file_w_name, 'r')
for line in fr:
    print(line)
