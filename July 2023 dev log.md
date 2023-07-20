# July 2023 Development Log

This log tracks the development of the Autosa software done in July of 2023 by Temba Mateke of Tenco.

## July 19 2023

This is the first day back since the summer of 2022. Need to re-oriente myself with the project.

### Hardware Connection

- don't remember how to connect over usb, the REAMDE doesn't say much in terms of connection set up or hardware requirements
- first step is to figure out how to do that then write it down for next time
- `instrument.py` has a line that checks for USB resources so I know at least that the connection to my computer was over USB, but I'm not sure if the other end on the EXA was USB or possibly ethernet
- I also really need to collect the documentation in the readme
- I noticed the back of the device has a "LAN/_USB symbol_" label above an ethernet port and a USB port. I'm going to try a USB-A to USB-A cable first and see if that works
- Reviewing this video: https://youtu.be/DUJpL9pMy8Y
- Connecting the USB-A to USB-A cable to the EXA and my computer didn't seem to work. I'm going to try a USB-B to USB-A cable next with the A end in my computer
- USB-B on EXA to USB-A on computer worked, I can see the instrument. I tested it as they suggested in the linked video.

```python
import pyvisa
rm = pyvisa.ResourceManager()
print(rm.list_resources())
```

- Tested with USB-A to USB-A, it does not work

### Autosa Testing

- Okay, I can see the instrument is detected when I run `main.py`, but nothing happens on the EXA. I know one likely reason is that the EXA does not have any of the configuration files on it that we had last time for testing. Hmm. I'm going to try and see if I can run in debug mode to see exactly what's going on.
- By the way, I have the 50 ohm resistor connected to the EXA
- PROGRESS! Was able to get the EXA to respond to commands! The response was "I can't find those files they don't exist" but that's a start.
- Need to make the program handle case where NI-VISA is not installed and case where instrument is not detected

### Final Notes for the Day

- I have to stop here today, was able to get Autosa to do several sanity checks before running
  - check if NI-VISA is installed
  - check that device is detected
  - check that folders in settings exist and contain the right files
- What I need to do now is finish off this last one by making it check the settings when you hit "Run" and not just when you save the settings (possible have it even run continously and display the errors in the window?)
- Then I need to clean up and commit
- After that, need to test that everything this far works as expected
- Then we can get to new features

## July 20 2023

Carrying on...

### Completing Settings Validation

- Validated settings in main window
- Now we need to be able to see the errors in the settings window before we even hit save
- Cleaned up a few other things, now ready to do new features
