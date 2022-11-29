# Autosa

Autosa is Tenco software used to automate data acquisition using a signal analyzer (AUTOmated Signal Analysis or AUTOmatic Signal Analyzer). The name is read as a single word with a stress on the second syllable.

# Installation

1. Install NI-VISA. This allows Autosa to communicate with the instrument.
2. Download the `install/dist/Autosa.exe` file from this repository and run

# Guiding Principles

This software is written to be as "plug-and-play" as possible. The more set up steps are required to use the software, the less likely it is to be used. This is why it comes packaged as an `.exe` file that just needs to be downloaded and double clicked. In this vein, all user interfaces should be as self-explanatory as possible.

# Development

- GUI is built with [pysimplegui](https://www.pysimplegui.org/en/latest/)
- Build is done with [pyinstaller](https://pyinstaller.org/en/stable/)

## Building

This project uses [PyInstaller](https://pyinstaller.org/en/stable/) to convert the python scripts and packages into a single, distributable `.exe` file.

The build is done by executing the `build.py` file. The output executable (`.exe`) file will be located in `root/install/dist`. The `/install/build` folder are the temporary files used by PyInstaller to create the executable. I don't know what the `.spec` file is, but it doesn't seem to be required to run the executable.

## Required Python Packages

- pyvisa
- pysimplegui
