#!/bin/bash

function usage() {
    cat <<USAGE
    
    Simple script to make a one-liner of personal remote creation on github. Best aliased to something short.
    
    Required: gh CLI, valid login, name arg.

    Usage: $0 [-n name] optional args: [-s] [-i] [-p] [-d description]

    Options:
        -n, --name=REPO_NAME             sets repo name
        -s, --show                       makes repo public
        -i, --init                       initializes git, adds all and commits 'init' before creating the remote 
        -p, --push                       pushes local to newly created remote
        -d, --descript=REPO_DESCRIPTION  sets repo description

        
USAGE
    exit 1
}

function init() {
    pwd -P | xargs -I %% git config --global --add safe.directory %%
    git init
    git add -A
    git commit -m "init"
}

function push() {
    git branch -M main
    git push -u origin main
}

function createGH() {
    echo $REPO_DESCRIPTION
    gh repo create $REPO_NAME -d="$REPO_DESCRIPTION" $VISIBILITY_FLAG $PUSH_FLAG -y

    if [ -n "PUSH_FLAG" ]; then
        push
    fi
}

if [ $# -eq 0 ]; then
    usage
    exit 1
fi

REPO_NAME=""
REPO_DESCRIPTION=""
VISIBILITY_FLAG="--private"
PUSH_FLAG=""

if [[ $# -eq 1 && "$1" != -* ]]; then
    REPO_NAME=$1
    createGH
    exit 1
fi

REPO_NAME=

while [ "$1" != "" ]; do
    case $1 in
    -n | --name)
        shift
        REPO_NAME=$1
        ;;
    -s | --show)
        VISIBILITY_FLAG="--public"
        ;;
    -i | --init)
        init
        ;;
    -p | --push)
        PUSH_FLAG="-s=. -r=origin"
        ;;
    -d | --descript)
        shift
        REPO_DESCRIPTION="$@"
        ;;
    -h | --help)
        usage
        exit 1
        ;;
    esac
    shift
done

if [ -z "$REPO_NAME" ]; then
    usage
    exit 1
fi

createGH
