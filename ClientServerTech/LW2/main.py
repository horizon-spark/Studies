import json
import yaml
import xml.etree.ElementTree as ET


def print_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(f"Reading {filename}...\n", data, end='\n\n')


def print_yaml(filename):
    with open(filename, mode='r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        print(type(data))
        print(f"Reading {filename}...\n", data, end='\n\n')


def print_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    print(f'Reading {filename}...')

    for child in root:
        print(child.tag, child.text)


def main():
    print_json('data.json')
    print_yaml('data.yaml')
    print_xml('data.xml')

if __name__ == '__main__':
    main()