# What is this?
Simple exporter to make obsidian .md files render as expected elsewhere.

Removes all custom markup - YAML frontmatter, tags, etc. 

## Why use it?
Obsidian is a very comfortable way to write and collect notes. It's very easy to decompose and summarize things, then reassemble something useful from the bits and pieces later. 

Importantly, you can write Latex (really MathJax) and have the results rendered as you're working. These formulas are rendered in any web-based client - notably VSCode, Github docs. That makes these files amazing references. You can bundle key formulas with natural language summaries alongside links to explanations. 

You can potentially create these markdown files more efficiently in VSCode, but for me these are separate modes. Obsidian is for brain dumps and creativity; VSCode is for implementation and getting things done. 

This exists so it's easy to convert the brain dumps into useful output, eg. creating documentation from notes, or sharing project ideas.

## How use it?
Pass the script an (obsidian) input directory and an output directory. All .md files in the input dir will be copied to the output, parsed for nice display on github.

```bash
obsidian-convert.py /path/to/folder/in/vault -o ./test
```
### On windows, you may need to amend the shebang 
```#!/usr/bin/env python```

or call python before running the script
```powershell
python obsidian-convert.py /path/to/folder/in/vault -o ./test
```

## But I don't use folders in Obsidian...
I probably shouldn't either.

If I make this a plug-in, I'll support exporting by tag.