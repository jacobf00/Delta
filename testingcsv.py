import csv

with open('sample.csv','r') as file:
    reader = csv.reader(file,delimiter=',')
    count = 0
    with open(r'data\test.csv','w') as newFile:
        writer = csv.writer(newFile,lineterminator='\n')
        for row in reader:
            count += 1
            if count > 1:
                row[0] = "John Stamos"
            writer.writerow(row)