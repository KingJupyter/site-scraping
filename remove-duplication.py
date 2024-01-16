import csv
import pandas as pd
from openpyxl import Workbook

def read_csv_to_list(file_path, encoding='latin-1'):
    data_list = []
    with open(file_path, 'r', encoding=encoding) as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data_list.append(row[0])
    return data_list

def read_xlsx_to_list(file_path, sheet_name):
    data_list = []
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    for column in df.columns:
        data_list.extend(df[column].tolist())
    return data_list

def  remove_items(list1, list2):
    return [item for item in list1 if item not in list2]

def convert_to_lowercase(lst):
    return [item.lower() for item in lst]

def write_list_to_csv(data_list, file_path):
    with open(file_path, 'w', newline='', encoding='latin-1') as file:
        writer = csv.writer(file)
        for item in data_list:
            writer.writerow([item])

def write_list_to_xlsx(data_list, file_path):
    workbook = Workbook()
    sheet = workbook.active
    for item in data_list:
        sheet.append([item])
    workbook.save(file_path)

surname_list1 = convert_to_lowercase(read_csv_to_list('surname.csv'))
# print(surname_list1)
surname_list2 = convert_to_lowercase(read_xlsx_to_list('surname.xlsx', 'surname'))
new_surname_list = remove_items(surname_list1, surname_list2)
print(new_surname_list)
print(len(surname_list1))
print(len(surname_list2))
print(len(new_surname_list))

write_list_to_csv(new_surname_list, 'newnames.xlsx')