param(
    [string]$name,
    [switch]$show,
    [switch]$init,
    [switch]$push,
    [string]$descript,
    [switch]$help
)

function Usage {
@"
    Simple script to make a one-liner of personal remote creation on github. Best aliased to something short.
    
    Required: gh CLI, valid login, name arg.

    Usage: ./<scriptname>.ps1 [-n name] optional args: [-s] [-i] [-p] [-d description]

    Options:
        -n, --name=REPO_NAME             sets repo name
        -s, --show                       makes repo public
        -i, --init                       initializes git, adds all and commits 'init' before creating the remote 
        -p, --push                       pushes local to newly created remote
        -d, --descript=REPO_DESCRIPTION  sets repo description
"@
    exit
}

function Init {
    git config --global --add safe.directory (Get-Location)
    git init
    git add -A
    git commit -m "init"
}

function Push {
    git branch -M main
    git push -u origin main
}

function CreateGH {
    Write-Output $REPO_DESCRIPTION
    gh repo create $REPO_NAME -d "$REPO_DESCRIPTION" $VISIBILITY_FLAG $PUSH_FLAG -y

    if ($null -ne $PUSH_FLAG) {
        Push
    }
}

if ($help) {
    Usage
    exit
}

if (!$name) {
    Usage
    exit
}

$REPO_NAME = $name
$REPO_DESCRIPTION = $descript
$VISIBILITY_FLAG = if ($show) {"--public"} else {"--private"}
$PUSH_FLAG = if ($push) {"-s=$((Get-Location).Path)\ "} else {""}

if ($init) {
    Init
}

CreateGH
