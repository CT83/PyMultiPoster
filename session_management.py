from flask import session

from json_management import list_to_json, json_to_list


def clear_session():
    session.pop('title', None)
    session.pop('post', None)
    session.pop('image', None)
    session.pop("selected_socialnetworks", None)


def save_session(filename, post, title, social_networks_list=None):
    if social_networks_list is None:
        social_networks_list = []
    session["title"] = title
    session["post"] = post
    session["image"] = filename
    if social_networks_list:
        store_list_session(social_networks_list)


def retrieve_session():
    title = session["title"]
    post = session["post"]
    filename = session["image"]
    return title, post, filename


def retrieve_session_socialnetworks():
    social_networks = session["selected_socialnetworks"]
    social_networks_list = json_to_list(social_networks)
    return social_networks_list


def remove_session_socialnetwork(s_name):
    social_networks = session["selected_socialnetworks"]
    social_networks = json_to_list(social_networks)
    s_name = str(s_name).lower()
    social_networks = [s.lower() for s in social_networks]
    print("Searching", s_name, "in", social_networks)
    if s_name not in social_networks:
        raise LookupError
    else:
        social_networks.remove(s_name)
        print("Returning", social_networks)
        return social_networks


def store_list_session(social_networks_list):
    session["selected_socialnetworks"] = str(list_to_json(social_networks_list))
