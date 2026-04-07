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
        print(f"Reading {filename}...\n", data, end='\n\n')


def print_xml_node(node, depth = 1):
    if len(node) > 0:
        print(f"{node.tag}:")
        for i in range(len(node)):
            print('\t' * depth, end='')
            print_xml_node(node[i], depth + 1)
    else:
        print(f"{node.tag}: {node.text}")


def print_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    print(f'Reading {filename}...')
    print_xml_node(root)


def main():
    print_json('data.json')
    print_yaml('data.yaml')
    print_xml('data.xml')

if __name__ == '__main__':
    main()