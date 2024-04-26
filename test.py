import csv

# Создаем словарь с данными
data = {'photo': "C:\\Users\\Алексей\\Downloads\\КИП2.jpg", 'category': "flow meter", 'serial_number': 2000,
                           'cost': 1000, 'service_life': 30, 'location': "main_storage",
                           'verification_date': "20.12.2013", 'responsible_person': "Alexei Stukaloff"}

with open('data.csv', 'w', newline='') as csvfile:
    fieldnames = list(data.keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow(data)
