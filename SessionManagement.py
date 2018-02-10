from flask import session


def clear_session():
    session.pop('title', None)
    session.pop('post', None)
    session.pop('image', None)


def save_session(filename, post, title):
    session["title"] = title
    session["post"] = post
    session["image"] = filename


def retrieve_session():
    title = session["title"]
    post = session["post"]
    filename = session["image"]
    return title, post, filename
