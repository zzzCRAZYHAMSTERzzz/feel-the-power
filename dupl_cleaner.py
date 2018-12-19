
def cleaner(file_name):
    
    unique_strings = set(open(file_name, 'r').readlines())
    new_file = open(file_name, 'w').writelines(unique_strings)
    #new_file.close()
    return(new_file)

cleaner('prices_2.txt')

f = open('prices_2.txt', 'r')
for line in f:
    print(line)

f.close()
