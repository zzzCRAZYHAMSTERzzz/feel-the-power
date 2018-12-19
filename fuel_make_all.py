import re
import csv
import os

def cleaner(file_name):
    
    unique_strings = set(open(file_name, 'r').readlines())
    new_file = open(file_name, 'w').writelines(unique_strings)
    return(new_file)

def look_for_no_price(line):
    result = re.sub(r'-.', '', line)

def look_for_no_comment(line):
    result = re.sub()


def split_date_time(line):
    new_date = ''
    pattern_day = re.findall(r'(\d{2})T\d{2}', line)
    pattern_time = re.findall(r'\d{2}T(\d{2})', line)
    if len(pattern_day) != 0 :
        new_date = pattern_day[0] + ',' + pattern_time[0]
    result = re.sub(r'\d{2}(T)\d{2}', new_date , line)
    return(result)

def make_nine_col(fr, fw):
    for line in fr:
        line = split_date_time(line)
        result = re.split(r',', line)
        if len(result) == 5:
            result.append('')
            result[5], result[4] = result[4], result[3]
            result[3] = ''
        
        if len(result) == 4:
            result.append('')
            result[4] = result[3]
            result[3] = ''
    
        if len(result) == 5:
            result[4] = result[4][0:-1]
            result.append('10:00:00')
        for i in range(len(result)):
            if result[i] == '–.':
                result[i] = ''
            if result[i] == '.':
                result[i] = ''
     
        if len(result) == 6:
            if result[5][-1] == '\n':
                result[5] = result[5][0:-1]
                
            result.append('')
            result.append('')
            result[7], result[6], result[5], result[4], result[3], result[2] = result[6], result[5], result[4], result[3], result[2], result[1]
            result[1] = ''
            result[7], result[6], result[5] = result[6], result[5], result[4]
            result[5] = ''
            result.append('YA_maps' + '\n')
        fw.write(','.join(result))



def debug_five_col(fr):
    count = 0
    for line in fr:
        result = re.split(r',', line)
        if len(result) == 5:
            count += 1
    print(count)


AI_80_pattern = re.compile('.*80[^\+]*')
AI_80_val = 'АИ-80'
AI_92_pattern = re.compile(r'.*92[^\+]*')
AI_92_val = 'АИ-92'
AI_92plus_pattern = re.compile('.*92\+.*')
AI_92plus_val = 'АИ-92+'
AI_95_pattern = re.compile('.*95[^\+]*')
AI_95_val = 'АИ-95'
AI_95plus_pattern = re.compile('.*95\+.*')
AI_95plus_val = 'АИ-95+'
AI_98_pattern = re.compile('.*98[^\+]*')
AI_98_val = 'АИ-98'
AI_98plus_pattern = re.compile('.*98\+.*')
AI_98plus_val = 'АИ-98+'
AI_100_pattern = re.compile('.*100[^\+]*')
AI_100_val = 'АИ-100'
AI_100plus_pattern = re.compile('.*100\+.*')
AI_100plus_val = 'АИ-100+'
METAN_pattern = re.compile(r'.*Метан')
METAN_val = 'Газ'
PROPAN_pattern = re.compile(r'.*Пропан')

PROPAN_val = 'Газ'
fuel_dict = {AI_80_pattern: AI_80_val,
             AI_92_pattern: AI_92_val,
             AI_92plus_pattern: AI_92plus_val,
             AI_95_pattern: AI_95_val,
             AI_95plus_pattern: AI_95plus_val,
             AI_98_pattern: AI_98_val,
             AI_98plus_pattern: AI_98plus_val,
             AI_100_pattern: AI_100_val,
             AI_100plus_pattern: AI_100plus_val,
             METAN_pattern: METAN_val,
             PROPAN_pattern: PROPAN_val
             }


#создадим функцию, приводящую различные варианты названий топлива к соответсвующему из словаря:
def format_price(fuel_name, fuel_dict):
    for key in fuel_dict.keys():
        result = key.search(fuel_name)
        if result is not None :
            if result.group(0) == fuel_name:
                fuel_name = fuel_dict[key]

    return(fuel_name)



def make_all(file_reading, file_writing, fuel_dict):
    reader = csv.reader(file_reading)
    for row in reader:
        writer = csv.writer(file_writing)
        for line in reader:
            if line != []:
                line[2] = format_price(line[2], fuel_dict)
                writer.writerow(line)
    return(reader)

    
csv_files = os.listdir(r'C:\Users\GPN-Centre\Desktop\parsing')
print(csv_files)

dir_name = 'cleaned_prices'

search_pattern = re.compile('.*_mapped.*')
for file in csv_files:
    if file[-4::] == r'.csv' and search_pattern.findall(file) is not None:
        print(file)
        fr = open(file, 'r')
        file_name = dir_name + '\\' + file[0:-4] + '_mapped.csv'
        fw = open(file_name, 'a', newline = '')
        make_all(fr, fw, fuel_dict)
        fr.close()
        fw.close()
        fr = open(dir_name + '\\' + file[0:-4] + '_mapped.csv', 'r')
        fw = open(dir_name + '\\' + file[0:-4] + '_mapped_cleaned.csv', 'w')
        make_nine_col(fr, fw)
        fr.close()
        fw.close()
        os.rename(file, 'parsed_prices\\' + file)
csv_files = os.listdir(r'C:\Users\GPN-Centre\Desktop\parsing\cleaned_prices')
search_pattern = re.compile('.*_mapped\.csv')
for file in csv_files:
    file_name = 'cleaned_prices' + '\\' + file
    if search_pattern.search(file_name) is not None:
        os.remove(file_name)


