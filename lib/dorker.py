import argparse

from dork.engine import DorkEngine

def do_args():
    parser = argparse.ArgumentParser(description='Your neighborhood dorking script.')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', dest='target', help='website to dork')
    group.add_argument('--worlist', dest='wordlist', help='list to dork')

    return parser.parse_args()

if __name__ == '__main__':
    args = do_args()
    if args.target:
        DorkEngine(args.target)
    elif args.wordlist:
        f = open(args.wordlist, 'r')
        for line in f.readlines():
            DorkEngine(line.strip())
