# this script takes a path to a .json, which is a set of notes (Mem, Google Keep, etc.), or objects,
# and converts each object into a markdown file with an appropriate filename,
# and includes relevant and available YAML frontmatter metadata.
# The script will return a directory of markdowns in the same directory as the source json.

import os
import re
import shutil
import json

# Define articles and prepositions
articles_prepositions_conjunctions = ['between', 'but', 'then', 'for', 'above', 'and', 'or',
                                      'an', 'a', 'into', 'so', 'at', 'from', 'to', 'before',
                                      'nor', 'by', 'yet', 'during', 'below', 'through', 'after',
                                      'the']


def create_file_name(title):
    # input should be the first line of the markdown

    # Convert title to lowercase
    title = title.lower()

    # Remove leading and trailing whitespaces
    title = title.strip()

    # Remove leading and trailing underscores
    title = title.strip("_")

    # Replace "/" with "-"
    title = title.replace("/", "-")

    # Replace spaces with "-"
    title = title.replace(" ", "-")

    # Replace "_" with "-"
    title = title.replace("_", "-")

    # Remove punctuation and non-alphanumeric characters
    title = re.sub(r'[^\w\s-]', '', title)

    # If title starts with "#", ensure it's followed by a digit
    if title.startswith("#") and (len(title) == 1 or not title[1].isdigit()):
        title = title[1:]

    # Remove "#" not followed by a digit
    title = re.sub(r'#\D', '', title)

    # Replace multiple consecutive "-" with a single "-"
    title = re.sub(r'-+', '-', title)

    # Title should not start with "-"
    while title.startswith("-"):
        title = title[1:]

    # Limit to 50 characters without cutting off words
    if len(title) > 50:
        title = title[:50].rsplit('-', 1)[0]

    # Title should not end with an article, preposition, or conjuncrion
    while '-' in title and title.rsplit('-', 1)[-1] in articles_prepositions_conjunctions:
        title = title.rsplit('-', 1)[0]

    # Title should not end with "-"
    while title.endswith("-"):
        title = title[:-1]

    return title + ".md"


def write_files_from_input_file(input_file_path):
    # Get directory of the input file
    global i
    input_dir = os.path.dirname(input_file_path)

    # Define output directory
    output_dir = os.path.join(input_dir, "mem_files_from_jason")

    # Clean the output directory before creating new files
    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(output_dir, exist_ok=True)

    try:
        with open(input_file_path, 'r') as file:
            # read json into memory
            mem_objects = json.load(file)
    except Exception as e:
        print(f"Failed to read file {input_file_path}: {e}")
        return []

    # Iterate through json for mems and create .md files
    for i, mem in enumerate(mem_objects):
        title = mem["title"]
        markdown = mem["markdown"]
        tags = mem["tags"]
        # cutting exact time from dates; "2023-08-02T23:24:39.690Z" becomes "2023-08-02"
        # and reformatting dates; "yyyy-mm-dd" becomes "mm-dd-yyyy"
        # created = reformat_date(mem["created"][:mem["created"].find("T")])
        # updated = reformat_date(mem["updated"][:mem["updated"].find("T")])
        # I found out Linter (community plugin) automatically reformat dates w/ times
        created = mem["created"]
        updated = mem["updated"]

        # Create the .md file name
        file_name = create_file_name(title)

        # Create the .md file and write the mem into it
        try:
            with open(os.path.join(output_dir, file_name), 'w') as file:
                # add YAML metadata: tags, title, created, updated; note Linter still needs to be configured.
                file.write(f"---\ntags: {tags}\ntitle: {title}\ncreated: {created}\nupdated: {updated}\n---\n")
                # add note
                file.write(markdown)
                # add tags for Obsidian
                file.write("\n")
                for tag in tags:
                    file.write(f"#{tag}\n")
        except Exception as e:
            print(f"Failed to write file {file_name}: {e}")

    # count mems for debugging
    counter = i
    # print count for debugging
    print(f"{counter} objects in input file.")

    # Return the list of files created
    return os.listdir(output_dir)


def reformat_date(date):
    # Split the date string into its components
    year, month, day = date.split("-")

    # Reformat and return the date
    return f"{month}-{day}-{year}"


input_file_path = '/home/ethan/Desktop/allMems.json'
output_files = write_files_from_input_file(input_file_path)
print(f"{len(output_files)} files created in the same directory as the input file.")
