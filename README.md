Usecase : you just need to have that file sent over to the Amiga, and you have MIDI. 
You do not want to swap floppies, you don't have disks or any other connection to the Amiga.

1. On the Amiga side make sure you have enough RAM. like 2 MB and more. 
   <b>! Somehow you manage to get MidiRecieveToRam.exe on a Workbench 3.1 disk with serial.device to work on your Amiga. </b>
2. You start MidiRecieveToRam.exe (from MIDIRECE.LHA) on your Amiga and have<br>
   <b>a Midi interface that connects your Amiga MIDI IN <-- to your PC MIDI OUT --> </b>
3. you drag and drop any file you want to send to the Amiga on the python script midi_to_amiga_final_dnd.py
4. select your Midi output device on the PC side, confirm, and ... wait for quite some time ...
5. Amiga side should show # chunk progress.
6. Very patiently wait for everything to unfold, it will take alot of time (15 minutes for 1,6 MB)
7. When done, check your Amiga RAM: disk, file should be there, test it, though! There is no error correction.
8. This is experimental software just for the fun of it. Use at your own risk.
9. Don't use it if you don't know what you're doing.
10. Modify all the things to your preferences, MIDIRECE.LHA contains the precompiled exe for Amiga1200, MIDIRECB.LHA contains the Blitz2 Source files.
11. midi_to_amiga_final_dnd.py is a Python 3 Script that requires:

(any OS) PC Side prerequisites:
Python: https://www.python.org/downloads/ --> 3.10
pip3 install rtmidi
pip3 install os
pip3 install time
pip3 install sys
pip3 install msvcrt
pip3 install mouse

Only if you want to code: Amiga Blitz Basic2: https://archive.org/details/ultimate-blitz-basic-v2_1
with this you can modify the Amiga (receiver side) to your preference.

(c)6/2025 by S.I.Hartmann aka WS, based on code by Claude Heiland-Allen https://mathr.co.uk/amiga/
