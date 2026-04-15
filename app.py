from flask import Flask, render_template, request, redirect, make_response
from datetime import datetime
import secrets
from db_manager import manage

app = Flask(__name__)

def set_token(username):
    token = secrets.token_hex(32)

    manage.add_token_to_db(token=token, username=username)
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

        username = request.form.get('username')
        user_email = request.form.get('email')
        data = [username, user_email]
        manage.add_to_db_user(data)

        response = set_token(username=username)
        return response

    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        get_cookie = request.cookies.get('user')

        if get_cookie is not None:
            #TODO: получать по этим куки информацию о пользователе из бд и отдавать их на index.html
            return redirect('/') # вернуть аккаунта пользователя
        else:
            return render_template('login.html')

    username = request.form.get('username')
    user_email = request.form.get('email')

    if manage.is_there_a_user_in_db(username=username) and user_email == manage.get_email(username=username):
        response = set_token(username)
        return response
    else:
        return render_template('registration.html')

if __name__ == '__main__':
    app.run(debug=True)