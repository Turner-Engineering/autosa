# Autosa

Autosa is Tenco software used to automate data acquisition using a signal analyzer (the name is spelled "Autosa" or "autosa" and is read as a single word with a stress on the second syllable).

## Setup

**Autosa has only been tested on Windows 10 and Windows 11 devices as of March 2026**

### Autosa Installation

This takes about 10 to 20 minutes, 1 reboot, and requires a decent internet connection.

1. Download and Install [NI-VISA](https://www.ni.com/en/support/downloads/drivers/download.ni-visa.html) for Windows (last tested version is 2025 Q4). This allows Autosa to communicate with the instrument.
   1. This will download the NI Package Manager from which you will install NI-VISA.
   2. You will be asked to disable windows fast startup - do this, it only affects boot from shutdown and not by much.
   3. Deselect ALL when it asks about additional packages, Autosa does not need them.
2. [Download the latest version](https://github.com/Turner-Engineering/autosa/releases/latest) of Autosa from this repository
   1. This link takes you to the "releases" page of this repository. From there, click "Autosa_vx.x.x.exe" under "Assets" to download the latest executable file.
   2. Autosa is not a "recognized" windows app, so you may get a warning about that, ignore the warning and run the executable. You may have to click "More Info" and then "Run Anyway" to get it to run.
3. Double click the executable file to run the program
   1. If the instrument is not connected, the program will start in Disconnected Mode.

### Instrument Setup

1. Make sure the instrument is plugged in to power and turned on.
2. Make sure the instrument is connected to this computer via USB-B (back of instrument) to USB-A (computer) cable. Alternatively, an ethernet cable can be used with an ethernet to USB-A/C adapter. See the images below.
3. Make sure the signal analyzer program is running on the device (called "LaunchXSA" on the instrument desktop)

<img src="https://github.com/ThisTemba/autosa/assets/36087610/0b688734-af36-4af1-bae5-a3874f0893b7" width="300px" alt="USB-B to USB-A cable" />

USB-B to USB-A Cable


<img width="3358" height="1890" alt="Ethernet to USB cable" src="https://github.com/user-attachments/assets/b6b97222-8d3f-405d-a989-7b30ac0942fd" />

Ethernet to USB-A/C Cable

### Connection Priority

Autosa auto-detects the instrument connection in this priority order:
1. **USB** - searches for USB resources
2. **Ethernet** - searches for TCPIP resources (excluding localhost)
3. **Emulator** - connects to `TCPIP0::localhost::inst0::INSTR`

If no connection is found, Autosa starts in **Disconnected Mode** which allows you to configure settings and view logs without an active instrument connection.

### Usage

There are five modes, accessible via tabs:

1. **Manual Mode** - start, stop, and save measurements manually. Good for railcar EMC tests where timing varies and tests are repeated depending on results.
2. **Single-Band Mode** - automatically loads state file, correction file, runs measurement, and saves trace + screenshot for a selected band. Good for running one band at a time.
3. **Multi-Band Mode** - runs multiple bands in sequence automatically, up to 5 consecutive runs with no intervention. Good for surveys when everything is set up and the procedure is repeated at each site.
4. **Set Up Mode** - update state files, adjust reference levels and offsets.
5. **Release Mode** - releases instrument control back to the front panel.

- It is best to set the local output folder to a cloud-synced folder like Dropbox or OneDrive so that the data is backed up automatically.

### Settings & Logs

- From within the app, open **Settings** (gear icon) and use the **"Open Settings File"** and **"View Logs"** buttons in the top right corner to view and manage settings and logs.
- Alternatively, paste `%LOCALAPPDATA%\Autosa` in the Windows Explorer address bar.
- All settings can be configured from within the app, but the settings file is a JSON file and can be edited directly if needed. 
- The logs are used for debugging and are not necessary for normal use. They can be shared with the developers if you encounter any issues.

## Development

### Guiding Principles

This software is written to be as "plug-and-play" as possible. The more setup steps are required to use the software, the less likely it is to be used. This is why it comes packaged as an `.exe` file that just needs to be downloaded and double clicked. In this vein, all user interfaces should be as self-explanatory as possible.

Different levels of automation are available for differing comfort levels and use-cases. The most automated mode performs up to 5 runs in a row with no intervention. This is good for surveys, when everything is set up correctly and the procedure is merely repeated at each site. The least automated mode functions almost as an extension of the instrument's physical interface, allowing the user to start, stop, and save data manually. This is good for railcar EMC tests where timing varies and tests are repeated depending on the results.

### Getting Started

Autosa is developed with Python 3.10.4 (other versions have not been tested). To run locally:

```bash
pip install -r requirements.txt
python src/main.py
```

If no instrument is connected, Autosa starts in **Disconnected Mode** — this is useful for UI development since all screens and settings are fully accessible. To test instrument communication without hardware, run a VISA emulator on localhost and Autosa will auto-detect it.

### Project Structure

- `src/main.py` — entry point: checks for NI-VISA, loads settings, detects instrument, launches UI
- `src/instrument/` — instrument communication (SCPI commands, file transfer, logging wrapper)
- `src/ui/` — all UI screens (one file per mode, plus settings, help, and popup windows)
- `src/utils/` — settings management, logging, warnings, stopwatch, run ID generation
- `src/build.py` — PyInstaller build script
- `src/autosa_version.txt` — single source of truth for version number
- `demo/` — demo state and correction files

### Packages

Core packages:

- [CustomTkinter](https://customtkinter.tomschimansky.com/) - user interface
- [PyInstaller](https://pyinstaller.org/en/stable/) - compiling to `.exe`
- [PyVISA](https://pyvisa.readthedocs.io/en/latest/) - instrument communication
- [Pillow](https://pillow.readthedocs.io/) - loading button icons
- [json_repair](https://github.com/mangiucugna/json_repair) - settings file validation
- [tzlocal](https://github.com/regebro/tzlocal) - timezone detection

### Building

This project uses [PyInstaller](https://pyinstaller.org/en/stable/) to convert the python scripts and packages into a single, distributable `.exe` file.

```bash
python src/build.py
```

The output executable will be at `install/dist/Autosa_v{version}.exe`. The `install/build` folder contains temporary PyInstaller files. The `.spec` file is auto-generated by PyInstaller and is not required to run the executable.

The version is read from `src/autosa_version.txt`.

### N9010B Reference Docs

Autosa was written to work with the N9010B signal analyzer. The [User's and Programmer's Reference](https://www.keysight.com/us/en/assets/9018-04666/user-manuals/9018-04666.pdf) was used to develop the SCPI commands. See [`screenshot_copy_example.md`](screenshot_copy_example.md) for a standalone PyVISA screenshot copy example.

### Terminology

`band_ori` = "v", "h"

`band_name` = B0, B1, B2, B3, B4, B5h, B5v, B6h, B6v, B7h, B7v

`band_key` = B0, B1, B2, B3, B4, B5, B6, B7

`run_id` = MMDD-## format (month/day-sequential number)

## Usage Record

- used Autosa in the field for the first time on October 18th 2023 for railcar tests.
- used Autosa in January 2024 for the NYCT Crane Car Test in New York City.
- used Autosa in January 2024 for the Toshiba Electric Locomotive Commissioning Tests in Taiwan.
- used Autosa in April 2024 for P2250 Railcar Tests in Pueblo, Colorado.
- used Autosa in June 2024 for PCEP survey
- used Autosa in February 2025 for MBTA GLTPS Survey
- used Autosa in June 2025 for PCEP survey 2
- used Autosa in October 2025 v0.3.0 and 0.4.3 (pre-release) for CTA RLE MLDB basline survey
- used Autosa in February 2026 v0.4.4 for NICTD Post-Energization Survey

## Notes

### May 24 2024

- added delay to run band, this should deal with the screenshotting of alerts with a small hit to time.

### June 5 2024

- Good thing that the file namer is based on the folders in the signal analyzer and not the folders on the test laptop. The test laptop can change within a single test, but only one SA will be used.

### October 23 2025

- Had some issues with the new version of Autosa, and with USB connections. Most of the 0.4.x bugs were fixed, USB still an issue. Had similar issue with fieldfox.
