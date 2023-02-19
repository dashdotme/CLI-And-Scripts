#!/usr/bin/env python3

import os
import argparse
import re

def insert_header(contents, filename):
    """Inserts filename as an h1 header at the start of the file, in the same way Obsidian displays it"""
    header = f"# {os.path.splitext(os.path.basename(filename))[0]}\n"
    if contents.startswith(header):
        return contents
    return header + contents


def space_separate_headers(contents):
    """Inserts newlines before headers if any are missing"""
    pattern = r"((?<!\n\n)#.*)"
    return re.sub(pattern, r"\n\n\1", contents)


def cleanup_tags(contents):
    """Cleans up tags"""
    pattern = r"\#[\w\-\/]+"
    return re.sub(pattern, "", contents)


def cleanup_frontmatter(contents):
    """Cleans up YAML frontmatter"""
    pattern = r"^---.*?---\n$"
    return re.sub(pattern, "", contents, flags=re.DOTALL | re.MULTILINE)


def cleanup_links(contents):
    """Cleans up internal links"""
    pattern = r"\[\[.*?\]\]"
    return re.sub(pattern, "", contents)


def fix_headers(contents):
    """Adds newlines before headers if any are missing"""
    pattern = r"(?<=\n)(\#{1,6}\s)" 
    return re.sub(pattern, r"\n\1", contents)


def downgrade_headers(contents):
    """Downgrades headers by one level"""
    pattern = r"(?:(?<=^)|(?<=\n))(\#{1,5}\s)"
    return re.sub(pattern, r"#\1", contents)

def amend_file(filename):
    """Inserts filename as an h1 header at the start of the file and calls other cleanup functions"""
    with open(filename, "r") as f:
        contents = f.read()

    # note: sequencing here is important
    contents = downgrade_headers(contents)
    contents = fix_headers(contents)
    contents = cleanup_frontmatter(contents)

    contents = insert_header(contents, filename)
    contents = cleanup_tags(contents)
    contents = cleanup_links(contents)

    return contents


def main():
    parser = argparse.ArgumentParser(
        description="Cleans up Obsidian markdown files to output as expected elsewhere"
    )
    parser.add_argument("input_dir", help="Directory containing input files")
    parser.add_argument(
        "-o",
        "--output_dir",
        default="output",
        help="Output directory (default: %(default)s)",
    )
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    for filename in os.listdir(args.input_dir):
        if filename.endswith(".md"):
            input_path = os.path.join(args.input_dir, filename)
            output_path = os.path.join(args.output_dir, filename)
            modified_contents = amend_file(input_path)
            with open(output_path, "w") as f:
                f.write(modified_contents)
            print(
                f"Successfully modified {input_path} and wrote result to {output_path}"
            )


if __name__ == "__main__":
    main()
