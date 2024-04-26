from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

# Пример начальных данных для таблицы
table_data = []

@app.route('/')
def index():
    return render_template('RESP.html')

@app.route('/table')
def table():
    with open('data.csv', mode='r') as file:
        reader = csv.reader(file)
        data = list(reader)
    return render_template('RESP2.html', data=data)

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Получение данных из формы
        photo = request.form['photo']
        category = request.form['category']
        serial_number = request.form['serial_number']
        cost = request.form['cost']
        service_life = request.form['service_life']
        location = request.form['location']
        verification_date = request.form['verification_date']
        responsible_person = request.form['responsible_person']

        # Добавление данных в таблицу
        table_data.append({'photo': photo, 'category': category, 'serial_number': serial_number,
                           'cost': cost, 'service_life': service_life, 'location': location,
                           'verification_date': verification_date, 'responsible_person': responsible_person})

        # Запись данных в CSV файл
        with open('data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([photo, category, serial_number, cost, service_life, location, verification_date, responsible_person])

        # Перенаправление на страницу с таблицей
        return redirect(url_for('table'))
    return render_template('RESP3.html')

if __name__ == '__main__':
    app.run(debug=True)
