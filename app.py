from flask import Flask, render_template, request
import datetime
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
        status_tool: bool = False
        completion_time: None = None

        return None

    return render_template('tasks.html')

@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    return render_template('statistics.html')

@app.route('/user', methods=['GET', 'POST'])
def user():
    return render_template('user.html')


if __name__ == '__main__':
    app.run(debug=True)