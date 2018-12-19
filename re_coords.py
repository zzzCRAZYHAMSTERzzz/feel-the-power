import re
from selenium import webdriver
import xlrd

def get_coords(url):
    
    temp_coords = str(re.findall(r'Bpoint%5D=\d{2}.\d{6}%2C\d{2}.\d{6}', url))
    coords = str(re.findall(r'5D=(\d{2}.\d{6})', temp_coords)[0]) + ', ' + str(re.findall(r'2C(\d{2}.\d{6})', temp_coords)[0])
    
    return(coords)


excel_directory = xlrd.open_workbook('AZS_directory.xlsx')
sheet = excel_directory.sheet_by_index(0)

f = open('directory.csv', 'w')
f.write('AZS_id' + ',' + 'AZS_name' + ',' + 'AZS_address' + ',' + 'YA_link' + ',' + 'Our_AZS' + ',' + 'Coords_1' + ',' + 'Coords_2' + '\n')
for i in range(1, sheet.nrows):
    try:
        st_url = str(sheet.row(i)[3])[6:-1]
        coords = get_coords(st_url)
    except IndexError:
        coords = ''
    csv_string = str(sheet.row(i)[0])[7:-2] + ',' + str(sheet.row(i)[1])[6:-1] + ',' + str(sheet.row(i)[2])[6:-1] + ',' + st_url + ',' + str(sheet.row(i)[4])[7:-2] + ',' + coords + '\n'
    f.write(csv_string)

f.close()
f = open('directory.csv', 'r')
for line in f:
    print(line)

f.close()

    



