# My scripts

This is a quick public dumping ground for simple scripts I've found widely useful.

# gh_create_repo.sh

Creates a new remote with the given name.

Optionally:

- initializes, adds all, and commits 'init' (-i)
- pushes local git to new remote (-p)
- makes repo public (-s)

### Requirements

[GH CLI set with auth token.](https://docs.github.com/en/github-cli/github-cli/quickstart)

# mygpt.py

Runs a given prompt through a gpt-3 model (davinci-3 completion by default).

Customize the defaults if you want it cheaper to suit your preferences. Looping completions with alternate models may get better results.

Prompts can be arbitrary length strings or files. Use files for anything the bash interpreter struggles with (ie. quotes)

### Requirements (Linux)

- install python3, pip if missing
- generate api key @ https://platform.openai.com/account/api-keys

```bash
pip install openai # or update if you're on version <0.27.x
echo "OPENAI_API_KEY=TOKENGOESHERE" | sudo tee -a /etc/environment
source /etc/environment
```

# Suggested use

Read (!), customize to your liking, then put any scripts you might use somewhere on your path with a short alias. I.e

```bash
chmod +x gh_create_repo.py
cp gh_create_repo.py ~/bin/ghcreate
# gcreate -n repo -i -p -s -d "My repo description"
```
