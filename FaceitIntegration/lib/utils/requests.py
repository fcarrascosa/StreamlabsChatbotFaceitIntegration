import json


def parse_json(string):
    return json.loads(string)


def make_get_request(parent, url, api_key=None, headers={}):
    request_headers = headers.copy() if headers else {}

    if api_key:
        request_headers.update({
            'Authorization': 'Bearer ' + api_key
        })

    request = parent.GetRequest(url, request_headers)
    parsed_request = parse_json(request)
    response = parse_json(parsed_request['response'])

    return response
