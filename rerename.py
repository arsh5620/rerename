#!/usr/bin/python
import sys
import os
import re

if __name__ == "__main__":
    arguments = sys.argv[1:]

    if arguments[0] == "-h" or arguments[0] == "--help":
        print(
            """re-rename:
The script works by searching for a regex in the file names for all the files in the current folder and substituing that found regex in the dest name and using that as new file name.
For example, source-regex "\sPhoto.*?\s", and dest-name "Pic{0}" will rename "DSLR Photo100.jpeg" to "Pic100.jpeg"
""")
        exit(0)

    if len(arguments) != 2:
        print(
            f"Usage: {sys.argv[0]} <source-regex> <dest-name>\nDestination name must contain '{0}' which will be substituted for regex matches")
        exit(1)

    source_regex = arguments[0]
    dest_name = arguments[1]

    if dest_name.find("{0}") == -1:
        print(
            "Destination regex must contain '{0}' which will be substitued for matches to regex")
        exit(1)

    files = [f for f in os.listdir('.') if os.path.isfile(f)]

    name_maps = {}

    print("Files to be renamed: ")
    for file in files:
        match = re.search(source_regex, file)
        if match:
            filename, file_extension = os.path.splitext(file)
            dest_filename = dest_name.replace("{0}", match.group())
            name_maps[file] = f"{dest_filename}{file_extension}"
            print(f"{file} -> {name_maps[file]}")

    if len(name_maps) == 0:
        print("No files to rename. Exiting.")
        exit(0)

    response = input("Do you want to commit the changes? (y/n)")
    if response == 'y' or response == 'Y':
        for original_name, new_name in name_maps.items():
            try:
                os.rename(original_name, new_name)
            except Exception:
                print(
                    f"Failed while trying to rename '{original_name}' to '{new_name}'")
    else:
        print("Changes were not commited. Aborting.")
