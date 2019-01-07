import os

data = ['hostnames', 'info', 'data', 'version']
def handle(output, persistence):
    path = "outputs/{}".format(output['path'])

    to_queue = []
    for match in output['matches']:
        filename = "{}-{}-{}".format(match['_shodan']['id'], match['ip_str'], match['port'])
        full_path = os.path.join(path, filename)
        if persistence.contains(full_path):
            continue
        to_write = "Entry: {}:{}<br>".format(match['ip_str'], match['port'])
        for piece in data:
            to_write += printif(piece, match)
        persistence.put_new(full_path, to_write)
        to_queue.append(to_write)
    return to_queue

def printif(key, json):
    if key in json:
        return ("{}: {}<br>".format(key.upper(), json[key]))
    return ''
