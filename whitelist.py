#!/usr/bin/env python3
import json
import os
import platform
import sys
import urllib.request

system = platform.system()
if system == 'Linux':
    def clear(): return os.system('clear')
elif system == 'Windows':
    def clear(): return os.system('cls')

api = 'https://api.mojang.com/users/profiles/minecraft/'
OK = 200

if len(sys.argv) < 3:
    print('Usage:')
    print(f'\t{sys.argv[0]} <filepath> <pop | add>')
    print()
    exit(1)


def open_json(path):
    with open(path, 'r') as f:
        try:
            return json.load(f)
        except:
            return []


def separator():
    print('------------------------------------')


def show(whitelist):
    clear()
    separator()
    for player in whitelist:
        print(player['name'])
        print(player['uuid'])
        separator()
    print()
    print(f'Players: {len(whitelist)}', end='\n\n')


def save(whitelist):
    with open('whitelist.json', 'w') as f:
        json.dump(whitelist, f, indent=2)


def add_player(whitelist: list):
    name = input('Add player: ')
    resp = urllib.request.urlopen(api + name)

    if resp.getcode() is OK:
        player: dict = json.loads(resp.read())
        player['uuid'] = player.pop('id')

        if not any(p['uuid'] == player['uuid'] for p in whitelist):
            whitelist.append(player)


def pop_player(whitelist):
    name = input('Remove player: ')
    whitelist = list(filter(lambda p: p['name'] != name, whitelist))
    return whitelist


def main():
    path = sys.argv[1]
    op = sys.argv[2]

    whitelist = open_json(path)
    length = len(whitelist)
    while True:
        try:
            show(whitelist)
            if op == 'pop':
                whitelist = pop_player(whitelist)
            elif op == 'add':
                add_player(whitelist)
            if len(whitelist) != length:
                save(whitelist)
            length = len(whitelist)
        except KeyboardInterrupt:
            clear()
            exit(0)
        except Exception as e:
            print('Woops, somethings wrong :S', end='\n\n')
            print(e)


if __name__ == '__main__':
    main()
