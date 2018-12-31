import argparse

from dork.engine import DorkEngine

def do_args():
    parser = argparse.ArgumentParser(description='Your neighborhood dorking script.')

    parser.add_argument('--url', dest='target', help='website to dork', required=True)

    return parser.parse_args()

if __name__ == '__main__':
    args = do_args()

    x = DorkEngine(args.target)
