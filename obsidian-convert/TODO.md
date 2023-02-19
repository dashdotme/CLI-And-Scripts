# Quick list of extensions

Nothing here is guaranteed or even likely. Just a record of ideas. Will implement as I find a use for them.

- [ ] support individual file conversion
- [ ] support recursive conversion
    - to allow quick conversion & upload of entire vaults
    - good alternative to 'Obsidian publish' for sharing personal docs/notes among a team
- [ ] auto-upload to git
    - ie. pipe to gh_create_repo.sh
- [ ] Obsidian integration as plug-in
    - ie. add 'export for git/vscode' button
    - [ ] add 'export by tag'
    - [ ] add 'compose' feature
        - ie. concatenate notes into single uber file
        - maybe just insert entire notes when `![[]]` is read?
- [ ] add config flags
    - eg. to retain YAML frontmatter, which some markdown clients render nicely
- [ ] export by tag
- [ ] optionally pipe through chatgpt for proofing
    - is this a good idea? Who knows, but it's trendy
- [ ] preserve valid internal links

### Should I be doing this all in typescript? 
Probably. Can do later. Python easy. At least it's not all in bash.