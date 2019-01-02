import os

HTML_FMT = """<html>
{}
</html>
"""
data = ['hostnames', 'info', 'data', 'version']
def handle(output):
    path = "outputs/{}".format(output['path'])

    if not os.path.exists(path):
        os.makedirs(path)

    for match in output['matches']:
        filename = "{}-{}-{}.html".format(match['_shodan']['id'], match['ip_str'], match['port'])
        full_path = os.path.join(path, filename)
        if os.path.exists(full_path):
            continue
        f = open(full_path, 'w')
        to_write = "Entry: {}:{}<br>".format(match['ip_str'], match['port'])
        for item in data:
            to_write += printif(item, match)
        f.write(HTML_FMT.format(to_write))
        f.close()

def printif(key, json):
    if key in json:
        return "{}: {}<br>".format(key.upper(), json[key])
    else:
        return ''
