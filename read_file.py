import fileinput
import json
import codecs


def format_data(filename):
    attrs = [
        'ts',
        'userId',
        'sessionId',
        'page',
        'auth',
        'mod',
        'status',
        'level',
        'itemInSession',
        'location',
        'userAgent',
        'lastName',
        'firstName',
        'registration',
        'gender',
        'artist',
        'song',
        'length'
    ]

    data = ''
    for line in codecs.open(filename, "r", "utf_8" ):
        data_list = []
        json_decode = json.loads(line)
        for attr in attrs:
            try:
                data_list.append(json_decode[attr])
            except:
                data_list.append('')
        data = data + '\t'.join(str(e) for e in data_list) + "\n"

    return data
