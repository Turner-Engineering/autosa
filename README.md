# Autosa

Autosa is Tenco software used to automate data acquisition using a signal analyzer (AUTOmated Signal Analysis or AUTOmatic Signal Analyzer). This can be pronounced as "Auto Ess Ay" or "au'tosa" (I prefer this one)

# Development

- GUI can be built with python simple gui
- Build can be done with pyinstaller

## Building

This project uses [PyInstaller](https://pyinstaller.org/en/stable/) to convert the python scripts and packages into a single, distributable `.exe` file.

The build is done by executing the `build.py` file. The output executable (`.exe`) file will be located in `root/install/dist`. The `/install/build` folder are the temporary files used by PyInstaller to create the executable. I don't know what the `.spec` file is, but it doesn't seem to be required to run the executable.
