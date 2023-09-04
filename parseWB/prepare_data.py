import csv

def read_file():
    with open('gmotors-drom.csv', encoding='windows-1251') as  file:
        reader = csv.reader(file, delimiter=';')
        proxy = []
        for row in reader:
            for i in range(len(row)):
                if len(row[i]) > 250:
                    new = row.pop(i)
                    row.insert(i, new[:250])

            proxy.append(row)

    with open('gmotors-rewrite-2.csv', 'w', encoding='windows-1251') as f:
        writer = csv.writer(f, delimiter=';')
        for row in proxy:
            writer.writerow(row)
            for line in row:
                if len(line) > 250:
                    print('ERROR', len(line))


read_file()