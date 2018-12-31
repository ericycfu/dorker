INDENT_FMT = "      {}"
def handle(output):
    for match in output['matches']:
        print(" Entry: {}:{}".format(match['ip_str'], match['port']))
        printif('hostnames', match)
        printif('info', match)
        printif('data', match)
        printif('version', match)

def printif(key, json):
    if key in json:
        fmt_print("{}: {}".format(key.upper(), json[key]))

def fmt_print(str):
    print(INDENT_FMT.format(str))
