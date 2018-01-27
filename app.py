from datetime import datetime

from flask import Flask

app = Flask(__name__)


@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%h")

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>

    <img src="http://loremflickr.com/600/400" />
    """.format(time=the_time)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
