#!/usr/bin/env python3

import argparse
import os
import subprocess
import shlex
import sys

def usage():
    print('''Simple script to make a one-liner of personal remote creation on github. Best aliased to something short.

Required: gh CLI, valid login, name arg.

Usage: {} [-n name] optional args: [-s] [-i] [-p] [-d description]

Options:
    -n, --name REPO_NAME             sets repo name
    -s, --show                       makes repo public
    -i, --init                       initializes git, adds all and commits 'init' before creating the remote 
    -p, --push                       pushes local to newly created remote
    -d, --descript REPO_DESCRIPTION  sets repo description
    -h, --help                       show this help message and exit
'''.format(os.path.basename(__file__)))

def init_repo():
    run_command('git init')
    run_command('git add .')
    run_command('git commit -m "init"')

def push():
    run_command('git branch -M main')
    run_command('git push -u origin main')

def create_gh(repo_name, repo_description, visibility_flag, push_flag):
    cmd = f'gh repo create {repo_name} -d "{repo_description}" {visibility_flag}'
    if push_flag:
        cmd += ' -s . -r origin'
    run_command(cmd)

    if push_flag:
        push()

def run_command(command_str):
    command_args = shlex.split(command_str)
    result = subprocess.run(command_args, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr, end='', file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-n', '--name', dest='repo_name', help='sets repo name')
    parser.add_argument('-s', '--show', dest='visibility_flag', action='store_const', const='--public', default='--private', help='makes repo public')
    parser.add_argument('-i', '--init', dest='init_flag', action='store_true', help='initializes git, adds all and commits "init" before creating the remote')
    parser.add_argument('-p', '--push', dest='push_flag', action='store_true', help='pushes local to newly created remote')
    parser.add_argument('-d', '--descript', dest='repo_description', default='', help='sets repo description')
    parser.add_argument('-h', '--help', action='store_true', help='show this help message and exit')

    args = parser.parse_args()

    if args.help or not args.repo_name:
        usage()
        return

    if args.init_flag:
        init_repo()

    create_gh(args.repo_name, args.repo_description, args.visibility_flag, args.push_flag)

if __name__ == '__main__':
    main()

