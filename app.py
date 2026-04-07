from flask import Flask, render_template, request, redirect
import datetime

from db_manager import Manage

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        title: str = request.form.get('name_tools')
        desc: str = request.form.get('description')
        creation_time: datetime.datetime = datetime.datetime.now()
        status_task: bool = False
        completion_time: None = None

        return redirect('/')

    return render_template('tasks.html')

@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    return render_template('statistics.html')

@app.route('/user', methods=['GET', 'POST'])
def user():
    return render_template('user.html')


if __name__ == '__main__':
    manage = Manage()
    manage.create_connection()
    app.run(debug=True)