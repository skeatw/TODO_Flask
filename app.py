from flask import Flask, render_template, request, redirect, make_response, jsonify
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

def time_for_people(tasks):
    l = []
    for task in tasks:
        lst_task = list(task)
        dt = datetime.strptime(lst_task[3], '%Y-%m-%d %H:%M:%S.%f')
        dt_for_people =  dt.strftime('%d-%m-%Y %H:%M')
        lst_task[3] = dt_for_people
        l.append(lst_task)
    return l


@app.route('/')
def index():
    username = None
    tasks = None
    get_cookie = request.cookies.get('user')
    if get_cookie is not None:
        username = manage.get_username_by_token(get_cookie)
        tasks = manage.get_tasks_by_token(get_cookie)
    #TODO: изменить формат даты и времени у всех задача
    if tasks is not None:
        tasks = time_for_people(tasks)


    if username is None:
        return redirect('user')

    return render_template('index.html', username=username, tasks=tasks)

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        get_cookie = request.cookies.get('user')

        user_id = manage.get_id_by_token(get_cookie)
        title: str = request.form.get('name_tools')
        desc = None
        if request.form.get('description') != '':
            desc = request.form.get('description')

        creation_time: datetime = datetime.now()
        status_task: bool = False
        data = [title, desc, creation_time, status_task, user_id]
        manage.add_to_db_task(data)

        return redirect('/')

    get_cookie = request.cookies.get('user')
    if get_cookie is not None:
        username = manage.get_username_by_token(get_cookie)

    return render_template('tasks.html', username=username)

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
            return redirect('/')
        else:
            return render_template('login.html')

    username = request.form.get('username')
    user_email = request.form.get('email')

    if manage.is_there_a_user_in_db(username=username) and user_email == manage.get_email(username=username):
        response = set_token(username)
        return response
    else:
        return render_template('registration.html')

#TODO: Сделать маршрут, который будет "вызываться" при нажатии на кнопку "Завершить задачу" и будет изменять статус задачи в базе данных
@app.route('/complete/<int:task_id>', methods=['POST'])
def complete(task_id):
    manage.complete_task(task_id)
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)