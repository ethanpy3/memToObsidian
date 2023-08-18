# memToObsidian
A little script I wrote to convert my notes from Mem.ai (json) to markdown format readable by Obsidian.md

This script takes a path to a .json, which is a set of notes (Mem, Google Keep, etc.), or objects,and converts each object into a markdown file with an appropriate filename, and includes relevant and available YAML frontmatter metadata. The script will return a directory of markdowns in the same directory as the source json.
