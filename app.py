from flask import Flask, render_template

app = Flask(__name__)


@app.route('/facebook_login')
def facebook_login():
    return render_template('facebook_login.html', app_id='101206834030831')


def post_to_instagram():
    from InstagramAPI import InstagramAPI
    InstagramAPI = InstagramAPI("pyreserver.pseudtech@gmail.com", "cybertech83")
    InstagramAPI.login()  # login

    photo_path = 'temp.jpg'
    caption = "Sample photo"
    InstagramAPI.uploadPhoto(photo_path, caption=caption)


@app.route('/instagram_login')
def instagram_login():
    post_to_instagram()
    return render_template('instagram_login.html', app_id='101206834030831')


@app.route('/blogger_login')
def blogger_login():
    return render_template('blogger_login.html',
                           app_id='812327379487-ufpflghav3471e07q4pje6cg99t1r9bj.apps.googleusercontent.com	')


@app.route('/')
def homepage():
    return render_template('home.html', app_id='101206834030831')


@app.route('/google91e934bee0a01da8')
def google91e934bee0a01da8():
    return render_template('google91e934bee0a01da8.html')




if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
