import json


def parse_json(keyword_callback, json_str: str, required_fields=None, keywords=None):
    if required_fields is None:
        required_fields = []
    if keywords is None:
        keywords = []
    try:
        json_doc = json.loads(json_str)
    except json.decoder.JSONDecodeError:
        raise TypeError('Type of field is not str')
    for field in required_fields:
        if field in json_doc:
            try:
                keywords_list = json_doc[field].split(' ')
            except AttributeError:
                raise TypeError('Type of value is not str')
            for value in keywords_list:
                if value in keywords:
                    keyword_callback(field, value)


def keyword_handler(cur_field, cur_key):
    print(f'Value "{cur_key}" in field "{cur_field}"')
