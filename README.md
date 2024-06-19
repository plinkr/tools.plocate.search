# Add-on for LibreELEC/Kodi `plocate Search`

`plocate Search` | `tools.plocate.search` is a LibreELEC/Kodi add-on designed to provide efficient offline search functionality for your multimedia library. By leveraging [`plocate`](https://plocate.sesse.net/) and [`updatedb`](https://plocate.sesse.net/), this add-on allows you to quickly locate files within your library, even when offline. The add-on integrates seamlessly with Kodi, offering an intuitive graphical interface for searching and navigating your media files.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Offline Search:** Utilize [`plocate`](https://plocate.sesse.net/) to perform fast, offline searches within your multimedia library.
- **Database Updates:** Automatically update the search database when new storage devices are connected.
- **Flexible Search:** Search across multiple databases stored in a designated directory.
- **Intuitive Interface:** Easy-to-use search interface within Kodi.
- **File Navigation:** Navigate to directories or play files directly from the search results.
- **Order by Size:** Option to sort search results by file size.
- **Color-Coded Results:** Different colors for directories and files in search results.

## Installation

1. **Download the Add-on:**
   - Download the `tools.plocate.search.zip` file from the releases section of this repository.

2. **Install via Kodi:**
   - Open Kodi and navigate to `Add-ons`.
   - Select `Install from zip file`.
   - Locate and select the downloaded `tools.plocate.search.zip` file.
   - Wait for the add-on installed notification.

3. **Post-Installation Script:**
   - The installation process will automatically run a script to copy and modify necessary `udev` rules.
   - It will also make the `update_index.sh` script executable.

## Usage

1. **Search for Files:**
   - Open the `plocate Search` add-on from the Kodi Add-ons menu.
   - Enter your search query in the dialog box.
   - The search results will be displayed, showing the file paths.

2. **Ordering Results by Size:**
   - After search results are displayed, an option to order by size in descending order will be available.
   - Select this option to sort the results by file size.

3. **Navigate or Play Files:**
   - Select a file to play it directly.
   - Select a directory to open it in the Kodi Videos file browser.

## Configuration

- **Search Options:**
  - You can configure various search options through the add-on settings in Kodi.
  - Modify options such as case-insensitive searches, regular expressions, basename searches, displaying the full path of the item or just the base file name and parent, for displaying conveniently less info, and searching only currently connected devices or including disconnected ones.

- **Index Management:**
  - The add-on automatically handles index updates for connected storage devices.
  - Indexes are stored in `/storage/.kodi/addons/tools.plocate.search/resources/databases/`.
  - Each index is named after the UUID of the storage device partition, ensuring uniqueness for every drive you connect to your LibreELEC device.

## Dependencies

- **plocate:** plocate is a `locate` based on posting lists, completely replacing `mlocate` with a much faster (and smaller) index.
- **updatedb:** Utility to update the database used by `plocate`.
- **LibreELEC:** Built on LibreELEC 12.0.0 and depends on the `udev` rules at `/storage/.config/udev.rules.d/95-udevil-mount.rules` to index newly connected devices.

Provided in this repo are the binaries of `plocate` and `updatedb` version `1.1.22`, compiled for `aarch64`, compatible with **LibreELEC 12.0.0**.

## Contributing

We welcome contributions to `tools.plocate.search`. To contribute:

1. Fork the repository.
2. Create a new branch with a descriptive name and change what you want.
3. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### Additional Information

- **Automatic Database Updates:**
  - When a new storage device is connected, the add-on detects the device and runs `updatedb` to update the search index. It uses a custom `udev` rule at `/storage/.config/udev.rules.d/95-udevil-mount.rules` to run the script that updates the index for that partition, in the background using `/usr/bin/systemd-run --on-active=1` so it doesn't affect the normal operation of `udevil`.
  - The index is named using the UUID of the connected device partition to ensure uniqueness.

- **Efficient Search:**
  - By combining multiple `.db` files, searches span across all connected and previously indexed storage devices.
  - This ensures comprehensive search results for your entire multimedia library.

### Example Usage and Performance

Developed on a Raspberry Pi 4 with **LibreELEC 12.0.0** and **Kodi 21.0.0**, `plocate` scans and builds the index of a 5TB disk filled with multimedia (containing 17,502 files) in about 12 seconds on the first run:
```
LibreELEC:~ # time /storage/.kodi/addons/tools.plocate.search/resources/lib/updatedb --database-root /var/media/easystore/ --output /storage/plinkr/plocate/plocate.db
real 0m 12.10s
user 0m 0.64s
sys 0m 0.23s
```

Subsequent runs are faster, taking less than 1 second (depending on file changes):
```
LibreELEC:~ # time /storage/.kodi/addons/tools.plocate.search/resources/lib/updatedb --database-root /var/media/easystore/ --output /storage/plinkr/plocate/plocate.db
real 0m 0.77s
user 0m 0.54s
sys 0m 0.23s
```

### Development Notes

**This add-on is an early Beta version.** Although it works as intended, please bear in mind it's still a concept. If you find any issues, please report them here in this repository.

This add-on uses a modified version of `/usr/lib/udev/rules.d/95-udevil-mount.rules` copied to `/storage/.config/udev.rules.d/95-udevil-mount.rules` to run `updatedb` and create the index for the connected device after it has been mounted by `udevil`. The script runs in the background to avoid interfering with normal operations. 

The add-on for Kodi returns search results and allows you to open directories or play media files directly. Configuration options enable various `plocate` behaviors, such as case-insensitive searches, regular expressions, basename searches, and searching only currently connected devices or including disconnected ones. This last option is useful if you want to find some file on a disk that you had previously connected, but you are unsure on what drive it is.

Currently, there is an issue deleting the `/storage/.config/udev.rules.d/95-udevil-mount.rules` file after uninstalling, so if you uninstall the add-on, please delete the file by hand. You can do so from the shell:
```
LibreELEC:~ # rm /storage/.config/udev.rules.d/95-udevil-mount.rules
```

### TODO
- Make `plocate` a LibreELEC add-on, so it can support all its platforms.
- Right now `plocate` is compiled for `aarch64` and only tested on a Raspberry Pi 4; it should be compiled for more architectures, or at least write a how-to for compiling `plocate` for LibreELEC on any architecture, so you can do it yourself.
- Make an option to rebuild the index of any connected device from the configuration, on demand.
- Find a way to clean the custom `udev` rules after uninstallation.

For more details, please refer to the source code within this repository.
