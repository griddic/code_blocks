from pprint import pprint

import yaml
from python.yaml_injection.yaml_injector import InjectionLoader


def main():
    with open('main.yaml') as inn:
        loaded = yaml.load(inn, InjectionLoader)
    print(loaded)


def main1():
    with open('sub/main.yml') as inn:
        loaded = yaml.load(inn, InjectionLoader)
    pprint(loaded)


if __name__ == '__main__':
    main()
