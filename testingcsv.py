import csv

with open('sample.csv','r') as file:
    reader = csv.reader(file,delimiter=',')
    count = 0
    for row in reader:
        print(row)