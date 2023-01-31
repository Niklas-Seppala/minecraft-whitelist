#!/usr/bin/env python3
import json
import os
import platform
import sys
import urllib.request
from urllib.parse import quote
from urllib.error import HTTPError

system = platform.system()
if system == 'Linux':
    def clear(): return os.system('clear')
elif system == 'Windows':
    def clear(): return os.system('cls')

API = 'https://api.mojang.com/users/profiles/minecraft/'
PATH = 1


def open_json(path):
    with open(path, 'r') as f:
        try:
            return json.load(f)
        except:
            return []


def separator():
    print('------------------------------------')


def show(whitelist, op):
    clear()

    separator()
    op_title = ''
    if op == 'add':
        op_title = f'\033[92m  Add players \033[0m({len(whitelist)})'
    else:
        op_title = f'\033[91mRemove players \033[0m({len(whitelist)})'
    print(f'         {op_title}      ')
    separator()
    print('Exit: ctrl+c')
    print('Switch mode: enter')

    print()
    if (len(whitelist) > 0):
        separator()
    for player in whitelist:
        print(player['name'])
        print(player['uuid'])
        separator()


def save(file, whitelist):
    with open(file, 'w') as f:
        json.dump(whitelist, f, indent=2)


def add_player(player_name, whitelist: list):
    change = False

    try:
        resp = urllib.request.urlopen(API+quote(player_name))
        player: dict = json.loads(resp.read())
        player['uuid'] = player.pop('id')

        if not any(p['uuid'] == player['uuid'] for p in whitelist):
            whitelist.append(player)
            change = True

    except HTTPError as e:
        if e.code == 404:
            print('\033[91mName not found\033[0m', end='\n\n')
        if e.code == 400:
            print('\033[91mIllegal name\033[0m', end='\n\n')

    return whitelist, change


def pop_player(name, whitelist):
    whitelist = list(filter(lambda p: p['name'].upper() != name.upper(),
                            whitelist))
    return whitelist, True


def main():
    if len(sys.argv) < 2:
        print('Usage:')
        print(f'\tpython3 {sys.argv[0]} <filepath>', end='\n\n')
        exit(1)

    path = sys.argv[PATH]
    op = 'add'

    whitelist = open_json(path)
    change = True
    while True:
        try:
            if change:
                show(whitelist, op)
                change = False

            op_title = ''
            if op == 'add':
                op_title = '\033[92m> \033[0m '
            else:
                op_title = '\033[91m> \033[0m'

            usr_inpt = input(op_title)
            if op == 'pop':
                if usr_inpt.strip() == '':
                    op = 'add'
                    change = True
                    continue
                (whitelist, change) = pop_player(usr_inpt, whitelist)
            elif op == 'add':
                if usr_inpt.strip() == '':
                    op = 'pop'
                    change = True
                    continue
                (whitelist, change) = add_player(usr_inpt, whitelist)

            if change:
                save(path, whitelist)

        except KeyboardInterrupt:
            clear()
            exit(0)
        except Exception as e:
            print('Error:')
            print(e, file=sys.stderr)
            exit(1)


if __name__ == '__main__':
    main()
