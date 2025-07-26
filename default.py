import os

import xbmc
import xbmcaddon
import xbmcgui

from resources.lib.install import create_udev_rules_if_not_exists, check_and_fix_executable_permission, \
    create_database_dir_if_not_exists
from resources.lib.search import search_files, get_file_sizes, format_size

# Get the addon's configuration
addon = xbmcaddon.Addon()
show_only_filename_and_parent = addon.getSettingBool('show_only_filename_and_parent')
options = {
    'search_basename': addon.getSettingBool('search_basename'),
    'search_case_insensitive': addon.getSettingBool('search_case_insensitive'),
    'only_existing': addon.getSettingBool('only_existing'),
    'search_using_regex': addon.getSettingBool('search_using_regex')
}


def main():
    # Create the udev rules if it doesn't exist
    create_udev_rules_if_not_exists()
    # Check and fix the executable permission for the binary files
    check_and_fix_executable_permission()
    # Create the database directory if it doesn't exist
    create_database_dir_if_not_exists()
    # Create a dialog for search query input
    dialog = xbmcgui.Dialog()
    search_query = dialog.input("Enter search query")

    if search_query:
        try:
            # Perform the search and get the results
            results = search_files(options, search_query)

            if results:
                # Process the results for the selection dialog
                result_list = results.split('\n')
                # Remove empty results
                result_list = [result.strip() for result in result_list if result.strip()]

                if result_list:
                    if show_only_filename_and_parent:
                        # If show_only_filename_and_parent is true, show only the base names of the files and the parent
                        # folder containing it, applying color to folders
                        display_list = [
                            f"[COLOR blue]{'/'.join(result.split('/')[-2:])}[/COLOR]" if os.path.isdir(result)
                            else "/".join(result.split('/')[-2:])
                            for result in result_list
                        ]
                    else:
                        # Show the full path of the found item, applying color to folders
                        display_list = [
                            f"[COLOR blue]{result}[/COLOR]" if os.path.isdir(result)
                            else result
                            for result in result_list
                        ]

                    # Add the option to sort by size with colors at the end of the file list
                    display_list.append("[COLOR yellow]Order by size in descending order[/COLOR]")

                    selected = dialog.select(f"Search results for `{search_query}`", display_list)

                    if selected == len(display_list) - 1:
                        # Sort by size if the corresponding option is selected
                        file_sizes = get_file_sizes(result_list)
                        sorted_results = sorted(zip(result_list, file_sizes), key=lambda x: x[1], reverse=True)
                        result_list = [result[0] for result in sorted_results]
                        display_list = [
                            f"[COLOR blue]{'/'.join(result[0].split('/')[-2:])}[/COLOR]" if os.path.isdir(result[0])
                            else f"/".join(result[0].split('/')[-2:]) + f" | {format_size(result[1])}"
                            for result in sorted_results
                        ]
                        selected = dialog.select(f"Sorted results by size for `{search_query}`", display_list)

                    if selected != -1:
                        selected_result = result_list[selected]

                        if os.path.isdir(selected_result):
                            # Open the folder with the file browser
                            xbmc.executebuiltin(f'ActivateWindow(Videos,"{selected_result}")')
                        elif selected_result.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                            # Open the image with the image viewer
                            xbmc.executebuiltin(f'ShowPicture("{selected_result}")')
                        else:
                            # Play the media file, video or audio
                            xbmc.executebuiltin(f'PlayMedia("{selected_result}")')
                else:
                    dialog.ok("Search Results", "No results found")
            else:
                dialog.ok("Search Results", "No results found")
        except FileNotFoundError as e:
            dialog.ok("Error", f"An error occurred: {str(e)}")
        except Exception as e:
            dialog.ok("Error", f"An error occurred: {str(e)}")


if __name__ == '__main__':
    main()
