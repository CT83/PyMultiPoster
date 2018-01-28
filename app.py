from flask import Flask, render_template

app = Flask(__name__)


@app.route('/facebook_login')
def facebook_login():
    return render_template('facebook_login.html', app_id='101206834030831')


@app.route('/instagram_login')
def facebook_login():
    return render_template('instagram_login.html', app_id='101206834030831')


@app.route('/')
def homepage():
    return render_template('home.html', app_id='101206834030831')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
