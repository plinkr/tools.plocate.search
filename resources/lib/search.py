import os
import subprocess

from resources.config import plocate_path, database_dir


def search_files(options, query):
    # Get all files ending with .db in the specified directory
    database_files = [f for f in os.listdir(database_dir) if f.endswith('.db')]

    if not database_files:
        raise FileNotFoundError(
            f"No databases found in the addon `{database_dir}` directory.\n"
            "Try reconnecting the device.")

    # Create the variable database_path with the full path of the files separated by ':'
    database_path = ':'.join([os.path.join(database_dir, f) for f in database_files])

    # Define additional parameters
    case_insensitive = "--ignore-case"  # search case-insensitively
    basename = "--basename"  # search only the file name portion of path names
    only_existing = "--existing"  # print only entries that refer to files existing at the time locate is run
    search_using_regex = "--regex"  # interpret patterns as extended regexps (slow)

    # Build the command with the additional parameters and the query
    command = [plocate_path, '--database', database_path]

    if options.get('search_case_insensitive', False):
        command.append(case_insensitive)

    if options.get('search_basename', False):
        command.append(basename)

    if options.get('only_existing', False):
        command.append(only_existing)

    if options.get('search_using_regex', False):
        command.append(search_using_regex)

    # Add the search query
    command.append(query)

    # Execute the `plocate` command with the search pattern and options
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Decode the output
    output = result.stdout.decode('utf-8')

    # Return the output of `plocate`
    return output


def get_file_sizes(file_paths):
    file_sizes = []
    for path in file_paths:
        try:
            # Get the size of the file
            size = os.path.getsize(path)
        except (OSError, FileNotFoundError):
            size = 0
        file_sizes.append(size)
    return file_sizes


def format_size(size):
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PiB"
