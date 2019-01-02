import argparse
import yaml

from dork.engine import DorkEngine

def do_args():
    parser = argparse.ArgumentParser(description='Your neighborhood dorking script.')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', dest='target', help='website to dork')
    group.add_argument('--org', dest='org', help='org to dork')
    group.add_argument('--target-list', dest='target_list', help='list to dork')

    return parser.parse_args()

if __name__ == '__main__':
    args = do_args()
    engine = DorkEngine()
    if args.target:
        engine.dork_target(args.target, 'url')
    if args.org:
        engine.dork_target(args.org, 'org')
    if args.target_list:
        target_data = yaml.load(open(args.target_list, 'r'))
        for org in target_data:
            engine.dork_target(org, 'org')
            for url in target_data[org]:
                engine.dork_target(url, 'url', org=org)
    engine.dump_target()
