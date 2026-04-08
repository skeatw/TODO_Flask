from flask import Flask, render_template, request, redirect, make_response
from datetime import datetime
import secrets
from db_manager import Manage

app = Flask(__name__)

def set_token():
    token = secrets.token_hex(32)
    response = make_response(redirect('/'))
    response.set_cookie('user', token, max_age=60 * 60 * 24 * 5, httponly=True, secure=True)
    return response
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        title: str = request.form.get('name_tools')
        desc: str = request.form.get('description')
        creation_time: datetime = datetime.now()
        status_task: bool = False
        data = [title, desc, creation_time, status_task]

        return redirect('/')

    return render_template('tasks.html')

@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    return render_template('statistics.html')

@app.route('/user', methods=['GET', 'POST'])
def user():
    return render_template('user.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':

        response = set_token()

        m = Manage()

        username = request.form.get('username')
        user_email = request.form.get('email')
        data = [username, user_email]
        m.add_to_db_user(data)

        return response

    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        m = Manage()

        cookie = request.cookies.get('user')

        username = request.form.get('username')
        user_email = request.form.get('email')

        if cookie is None:

            response = set_token()


            return response

        else:
            user_email_from_db = m.get_email(username=username)
            if user_email_from_db == user_email:
                return redirect('/')
        #TODO: получить куки пользователя есть время куки не истекло, то сразу перейти в аккаунт, если истекло для пользователя с username должна совпадать отправленная им

    return render_template('login.html')

if __name__ == '__main__':
    manage = Manage()
    manage.create_connection()
    app.run(debug=True)