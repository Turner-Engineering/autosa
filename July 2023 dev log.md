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

### Feature 1: Individual Bands

We want a way to be able to run specific bands on command. The continous mode that is currently the only mode is good for surveys where timing doesn't matter much and we just have to get through all the bands. But for other tests, it is helpful to be able to run specific bands at specific times and to be able to repeat those runs.

The simplest version of this, would just run an individual band with all the current settings by clicking a specific button. The main issue I forsee is file naming, how do we ensure that files are named correctly and don't overwrite each other? Do we force the user to name every run? Do we check the instrument for files that are already saved there? Do we just append a number to the end of the file name?

Here is the plan for the MVP:

1. Add a button for each band to the main window
2. Make each button trigger that specific band using all the current settings
3. Don't worry about file names

#### 1.1 Rough Version

I created the rough version and yeah it works pretty nice. I've decied that I am going to make the filenames auto-increment the numbers based on the files that are stored on the machine. One failure mode of this is if you delete the files on the instrument during a test, you may get name conflicts. That could be quite a serious issue so I think it will need to confirm every single filename to make certain that never happens.

Before that though, I want to move the site name to settings, I think it makes more sense to have it there.

Done!

#### 1.2 File Naming

Next step is handling the filename convention. Here's the No. 1 rule: **DO NOT LOSE DATA!**. It is better to have badly named files that are all present than to have files overwriting other files. So the first step should be throwing an error if the system tries to overwrite data. The next step is creating some kind of file naming function that reads the files in the output folder, figures out what the new file should be called, and creates the filename. Finally, we need to have user-input to confirm that the filenames are correct. So we need a dialog that pops up when the user tries to start a run that says "this is what I'm going to call the file, you like?", then the user can modify the filename if they want.

- [x] throw error on overwrite attempt
- [x] make filename creator
- [x] confirm filename

## July 21 2023

Remember to reference the field guide!

### File Name Creator

We need to get the last run index:

1. Load the filenames in the output folder on the instrument into a list
2. Isolate the run ids from the filenames
3. Determine which is the latest run id
4. Extract the run index from the id

### Other helpful buttons

- Record Current Setup (this would just record for the sweep dur however the exa is set up, and will save items with the correct file name. So it basically skips the state and correction file loading steps)
- Save Current Data (this would be the second half of the record_and_save function, it would just take a screenshot, and save the trace to the computer and instrument)

### Orientation

- Added an orientation dropdown to the multi-band menu
- Just realized that the single band needs that too, probably just need to add three more buttons and have half labelled as v and the other as h. Only issues is then we don't have a nice grid of buttons. We would have 11 buttons.
- I could section that out into monopole and bilogic then have the bilogic section be two rows of three buttons
- I also really want to add the logo to the top left

### Next Steps

- next steps for tomorrow are to add the orientation to individual band running. Plan is to do it with three rows and two sections
- section 1 is one row of 5 for monopole
- Section 2 is two rows of 3 for bilogic, first row is h second is v

https://pyvisa.readthedocs.io/

## July 23 2023

### Some helpful features

I implemented a few helpful features:

1. Automatically set marker to peak
2. Automatically raise reference level if max is too high
3. Set tab name to band name
4. Add prep mode
5. Return to local mode on window close
6. Add orientation to single band buttons
7. Add more filename validation

## July 24 2023

It seems statefiles are more capable than I thought. The statefile can store coupling factors so we don't need that, and I think they can also store corrections.
I think correction files can be loaded into collection registers and state files and select which registers are active for which state.

- also the save screen config + state will save all the set up bands so that they don't have to be re-set up every time

## August 3 2023

- [x] Don't record with ref level offset

---

- [x] Have run note pop up as dialog in single band mode
- [x] Manual start stop for custom duration (have popup for file name here too)
- [x] "Save as is" button is good to have!
- [x] Merge prep band mode into manual mode (want to prepare then run, then save, and repeat)
- [ ] Fix settings so that they work on the first install

---

- [x] make sure state files are set up with 10s number y scale
- [x] Add auto marker positioning to manual mode
- [x] have trace closer to the top (don't leave 10 dB gap)
- [x] Save screenshot in light mode, leave instrument in dark mode
- [x] Close settings window on right before taking screenshot
- [x] Have a "release" tab / button to let go of the instrument and allow manual control

---

- [ ] Have a button to pull up all states in different tabs
- [ ] Have instructions to say that the state files should contain limit lines and BW
- [ ] Have setting to have marker auto peak off (low priority)
- [ ] Add indicator to say when instrument is under remote control

## Aug 4 2023

Notes:

- seems like USB-B 3.0 has some issues, recommend 2.0 till we can figure out what's going on

### State File Ispector

I think we want some kind of tool that says if the state files are set up correctly
