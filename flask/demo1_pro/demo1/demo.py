from flask import Flask,request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!<h1>' % name


@app.route('/ua')
def ua():
    ua = request.headers.get('User_Agent')
    return '<p>Your broswer is %s.<p>' % ua


if __name__ == '__main__':
    app.run(debug=True)
