import json


def list_to_json(inp):
    return json.dumps(list(inp))


def json_to_list(jn):
    return json.loads(str(jn))
