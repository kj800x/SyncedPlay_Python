# SyncedPlay

This program was developed for people who need to play back certain sound files at certain times, with no delay.
My particular use-case was during drama preformances, when sound effects had to be played, and other solutions had too long of a loading period.

## Prerequisites

*   Python 2.7 or similar (Other versions might work, but this is what I developed with.)
*   PyGame, compatable with your version of python

## Setup

1.  Convert audio files to "OGG" and place them in the sounds directory.
2.  Create the overall setting file, settings.txt (placed in the Settings directory)
3.  Decide on filenames for the 3 other settings files: your sound file, cue file, and layout file. Create them.

## Run

If you are on Linux or a Mac, you might be able to double click on "run.sh", or "code.py"
If you are on Windows, you might be able to double click on "code.py", otherwise, email kevin[at]coolkev . com and I'll try to help

If you press tab, you will run the current cue, and step down the list.
If you press enter, you will run the command that is currently in the prompt.
If you press any other key, you will type to the prompt.

### Commands

Commands are the basis of the program. Cues are just a collection of commands, pre-written out so that you just have to hit next.
Here are the current possible commands:

+   Close                 - Close the program
+   Exit                  - Close the program
+   Goto [Cue Number]     - Go to the specified cue number
+   Fade [seconds] [what] - Fade a sound over a certain number of seconds, "what" can be either "all" or the keyword for one of the sounds.
+   Silence [what]        - Immediately silence a sound, "what" can be either "all" or the keyword for one of the sounds.
+   Play [what]           - Begin playing a sound, "what" is a keyword for one of the sounds.
+   Loop [what]           - Begin looping a sound infinitly, "what" is a keyword for one of the sounds.

## Format for configuration files:

In all configuration files, blank lines and lines starting with # are ignored

### settings.txt (The overall setting file, filename hardcoded in)

All of these settings are required:

    num_channels = Number of channels to allocate. 30 is a safe number that most modern computers can handle.
    soundfile = Location of the sounds file.
    cuesfile = Location of the cues file.
    layoutfile = Location of the layout file.
    fullscreen = True or False. True is recommended
    windowwidth = 0 is the recommended setting, it will try to match the screen resolution.
    windowheight = 0 is the recommended setting, it will try to match the screen resolution.
    undefinedcolor = A hex color for the overall background. Format is like this "FF0000" for red.
    font = A font name. Monospaced fonts look much better
    fontsize = A font size.
    
Sample:

    num_channels = 30
    soundfile = ./sounds.txt
    cuesfile = ./cues.txt
    layoutfile = ./genericlayout.txt
    fullscreen = True
    windowwidth = 0
    windowheight = 0
    undefinedcolor = 96C4F2
    font = Courier New
    fontsize = 15

### The Sound File (Links sound files with keywords)

Sound file format:

    [Path To Sound File relative to the sounds directory]
    name = value
    keyword = value

Example sound file:

    [phonering.ogg]
    name = Phone Ringing
    keyword = phone
    
    [door_creaks.ogg]
    name = Door Creaking
    keyword = door

### The Cue File (A sequential list of events that happen in a show)

Sound file format:

    [Cue title]
    command to run

Example sound file:

    [Opening]
    play curtain_unravels
    play laugh_track
    
    [Ocean Scene Starts]
    loop waves
    play creaking_ship
    
    [End of show]
    play applause_track
    
    [Lights out]
    fade 1 all
    
### The Layout File (How the display will look)

Layout file format:

    [Section]
    key = value
    
Required keys:

+   x - where the left side of the section begins, as a percent of the screen (without percent sign)
+   y - where the top side of the section begins, as a percent of the screen (without percent sign)
+   width - width of the section, as a percent of the screen (without percent sign)
+   height - height of the section, as a percent of the screen (without percent sign)
+   backgroundcolor - background color of the section
+   bordercolor - border color of the section
+   bordersize - size of the border in pixels
+   padding - padding inside the border in pixels

Certain sections also require other keys:

+   Prompt:
+   +   color - color of the text, in hex, like so: "FF0000"
+   Response:
+   +   commandcolor - color of the command text, in hex, like so: "FF0000"
+   +   commandcolor - color of the response text, in hex, like so: "FF0000"
+   Cues:
+   +   color - color of the text, in hex, like so: "FF0000"
+   +   linespacing - spacing between lines, in pixels

Example layout file:

    [Prompt]
    x = 0
    y = 90
    width = 100
    height = 10
    backgroundcolor = 000000
    bordercolor = 5555FF
    bordersize = 3
    padding = 3
    
    color = 00AA00

    [Response]
    x = 70
    y = 0
    width = 30
    height = 90
    backgroundcolor = 000000
    bordercolor = 5555FF
    bordersize = 3
    padding = 3
    
    commandcolor = 00AA00
    responsecolor = FFFFFF

    [Cues]
    x = 0
    y = 0
    width = 70
    height = 90
    backgroundcolor = 000000
    bordercolor = 5555FF
    bordersize = 3
    padding = 3
    
    color = 00AA00
    linespacing = 3
