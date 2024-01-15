# Autosa

Autosa is Tenco software used to automate data acquisition using a signal analyzer (AUTOmated Signal Analysis or AUTOmatic Signal Analyzer). The name is spelled exactly as "Autosa" and is read as a single word with a stress on the second syllable.

## Getting Started

Windows is the recommended operating system for AutosaVersion 2022 Q3. It has not been tested on other operating systems.

### Autosa Installation

**Autosa has only been tested on Windows 10 and Windows 11 devices**

This takes about 10 to 20 minutes, 1 reboot, and requires a decent internet connection.

1. Download and Install [NI-VISA](https://www.ni.com/en/support/downloads/drivers/download.ni-visa.html) for Windows (last tested version was 2023 Q3). This allows Autosa to communicate with the instrument. Please read the instructions below for extra guidance.
   1. The link above will take you to the This will download the NI Package Manager from which you will install NI-VISA.
   2. You will be asked to disable windows fast startup - do this, it only affects boot from shutdown and not by much.
   3. Deselect ALL when it asks about additional packages, Autosa does not need them.
2. Download the executable file [`Autosa.exe`](https://github.com/ThisTemba/autosa/releases/tag/v0.3) from this repository
   1. This link takes you to the "releases" page of this repository. From here, click "Autosa.exe" under "Assets" to download the executable file.
   2. Autosa is not a "recognized" windows app, so you may get a warning about that, ignore the warning and run the executable. You may have to click "More Info" and then "Run Anyway" to get it to run.
3. Double click the executable file to run the program
   1. If the instrument is not connected, the program will start and say the instrument was not detected. See below for usage instructions

### Instrument Setup

1. Make sure the instrument is plugged in to power and turned on
2. Make sure the instrument is connected to this computer via USB-B (back of instrument) to USB-A (computer) cable. See image below.
3. Make sure the signal analyzer program is running on the device (called "LaunchXSA" on the desktop)

<img src="https://github.com/ThisTemba/autosa/assets/36087610/0b688734-af36-4af1-bae5-a3874f0893b7" width="300px" />

Required USB-B to USB-A cable

## Development

### Guiding Principles

This software is written to be as "plug-and-play" as possible. The more set up steps are required to use the software, the less likely it is to be used. This is why it comes packaged as an `.exe` file that just needs to be downloaded and double clicked. In this vein, all user interfaces should be as self-explanatory as possible.

Different levels of automation are available for differing comfort levels and use-cases. The most automated mode performs up to 5 runs in a row with no intervention. This is good for surveys, when everything is set up correctly and the procedure is merely repeated at each site. The least automated mode functions almost as an extension of the instrument's physical interface, allowing the user to start, stop, and save data manually. This is good for railcar EMC tests where timing varies and tests are repeated depending on the results.

### Packages

The following packages are required for development:

- [pysimplegui](https://www.pysimplegui.org/en/latest/) - creating user interface
- [pyinstaller](https://pyinstaller.org/en/stable/) - compiling python scripts `.exe` file
- [pyvisa](https://pyvisa.readthedocs.io/en/latest/) - communicating with the instrument over USB

Install all three with pip:

```bash
pip install pysimplegui pyinstaller pyvisa
```

### Building

This project uses [PyInstaller](https://pyinstaller.org/en/stable/) to convert the python scripts and packages into a single, distributable `.exe` file.

The build is done by executing the `build.py` file. The output executable (`.exe`) file will be located in `root/install/dist`. The `/install/build` folder are the temporary files used by PyInstaller to create the executable. I don't know what the `.spec` file is, but it doesn't seem to be required to run the executable.

## Real World Tests

### October 2023

Tenco used Autosa in the field for the first time on October 18th 2023 for railcar tests.
