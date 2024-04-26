from datetime import datetime

from flask import render_template, redirect, request, Flask, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Допустимые значения для логина и пароля
VALID_USERNAME = "mechanic"
VALID_PASSWORD = "2000"


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    serial = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    time = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    person = db.Column(db.String(100), default=datetime.utcnow)

    def __repr__(self):
        return '<device %r>' % self.id


@app.route('/')
def index():
    return render_template("RESP.html")


@app.route('/table', methods=['GET', 'POST'])
def table():
    if request.method == 'POST':
        id = request.form["id"]
        photo = request.form["photo"]
        category = request.form["category"]
        serial = request.form["serial"]
        price = request.form["price"]
        time = request.form["time"]
        location = request.form["location"]
        date = request.form["date"]
        person = request.form["person"]

        device = Device(id=id, photo=photo, category=category, serial=serial, price=price,
                        time=time, location=location, date=date, person=person)
        try:
            db.session.add(device)
            db.session.commit()
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()

    devices = Device.query.all()
    return render_template('RESP2.html', device=devices)


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            return redirect(url_for('form'))
        else:
            error_message = "Неверный логин или пароль"
            return render_template('login.html', error_message=error_message)
    return render_template('login.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        id = request.form.get('id')
        device = Device.query.filter_by(id=id).first()
        if device:
            try:
                db.session.delete(device)
                db.session.commit()
                return redirect(url_for('index'))
            except Exception as e:
                error_message = f"Ошибка при удалении: {str(e)}"
                return render_template('delete.html', error_message=error_message)
        else:
            error_message = "Объект с таким ID не найден"
            return render_template('delete.html', error_message=error_message)
    return render_template('delete.html')


@app.route('/save_data', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Получение данных из формы
        id = request.form['id']
        photo = request.form['photo']
        category = request.form['category']
        serial = request.form['serial']
        price = request.form['price']
        time = request.form['time']
        location = request.form['location']
        date = request.form['date']
        person = request.form['person']
        device = Device(id=id, photo=photo, category=category, serial=serial, price=price,
                        time=time, location=location, date=date, person=person)
        try:
            db.session.add(device)
            db.session.commit()
            return redirect("/table")
        except:
            return "При загрузке данных произошла ошибка"
    else:
        return render_template('RESP3.html')


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
