from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        return render_template('tasks.html')

    return render_template('tasks.html')

@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    return render_template('statistics.html')

@app.route('/user', methods=['GET', 'POST', 'UPDATE'])
def user():
    return render_template('user.html')


if __name__ == '__main__':
    app.run(debug=True)