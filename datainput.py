import csv
import os

folder_path = 'F:\\Complete\\phone-scraping\\files\\@all\\New folder'
file_names = os.listdir(folder_path)


previous_cnt = 0
unvalid_cnt = 0
total_cnt = 0
current_cnt = 0

with open('database.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    phone_to_city = {}
    for row in reader:
        previous_cnt += 1
        phone_to_city[row['phone']] = row['city']

# print('reading database success')

# import csv
for file_name in file_names:
    # print(file_name)
    with open(os.path.join(folder_path, file_name), 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_cnt += 1
            number = row['PhoneNumber']
            city = row['Address']
            phone_number = "36" + number.replace(" ", "")
            # phone_number = number.replace(" ", "").replace('+', '')
            if(len(phone_number) != 11):
                unvalid_cnt += 1
                continue
            phone_to_city[phone_number] = city
    # print('reading ' + file_name + ' success')

# print('writing')

# Write the updated dictionary back to the CSV file
with open('database.csv', 'w', newline='', encoding='utf-8-sig') as f:
    fieldnames = ['phone', 'city']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()  # Write the header
    for phone, city in phone_to_city.items():
        current_cnt += 1
        writer.writerow({'phone': phone, 'city': city})

#  result output

print('operation success')
print('Previous numbers: ' + str(previous_cnt))
print('Total numbers: ' + str(total_cnt))
print('Unvalid numbers: ' + str(unvalid_cnt))
print('Current numbers: ' + str(current_cnt))
print('Duplication numbers: ' + str(total_cnt - current_cnt + previous_cnt - unvalid_cnt))
print('Increased numbers: ' + str(current_cnt - previous_cnt))
print('Success ratio: ' + str((current_cnt - previous_cnt)/(total_cnt)*100) + '%')
print('New numbers: ' + str(current_cnt - 670020))
