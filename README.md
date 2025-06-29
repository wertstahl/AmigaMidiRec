<b>AmigaMidiRec - Transfer File from any OS to Amiga via MIDI</b><br>
<br>
<b>Usecase :</b> <i>you need to have that file sent over to the Amiga, and you have MIDI.<br> 
You do not want to swap floppies, you don't have disks or any other connection to the Amiga.</i><br>
<br>
1. On the Amiga side make sure you have enough RAM. Like 2 MB and more. <br>
   <b>! Somehow you manage to get MidiRecieveToRam.exe on a Workbench 3.1 disk with serial.device to work on your Amiga. </b>
2. You start MidiRecieveToRam.exe (from MIDIRECE.LHA) on your Amiga and have<br>
   <b>a Midi interface that connects your Amiga MIDI IN <-- to your PC MIDI OUT --> </b>
3. you drag and drop any file you want to send to the Amiga on the python script midi_to_amiga_final_dnd.py<br>
4. select your Midi output device on the PC side, confirm, and ... wait for quite some time ...<br>
5. Amiga side should show # chunk progress.<br>
6. Very patiently wait for everything to unfold, it will take alot of time (15 minutes for 1,6 MB)<br>
7. When done, check your Amiga RAM: disk, file should be there, test it, though! There is no error correction.<br>
8. This is experimental software just for the fun of it. Use at your own risk.<br>
9. Don't use it if you don't know what you're doing.<br>
10. Modify all the things to your preferences, MIDIRECE.LHA contains the precompiled exe for Amiga1200, MIDIRECB.LHA contains the Blitz2 Source files.<br>
11. midi_to_amiga_final_dnd.py is a Python 3 Script that requires:<br>
<br>
(any OS) PC Side prerequisites:<br>
Python: https://www.python.org/downloads/ --> 3.10<br>
pip install: <br>
rtmidi<br>
os<br>
time<br>
sys<br>
msvcrt<br>
mouse<br>
<br>
if you want to code: Amiga Blitz Basic2: https://archive.org/details/ultimate-blitz-basic-v2_1<br>
with this you can modify the Amiga (receiver side) to your preference.<br>
<br>
(c)6/2025 by S.I.Hartmann aka WS, based on code by Claude Heiland-Allen https://mathr.co.uk/amiga/<br>
<br>
NOTE: this was only tested on real hardware. No idea if a loopback from WINUAE to local OS actually works. If you had any success with that, let me know.<br>
NOTE2: The files you would most likely want to try out are https://github.com/wertstahl/AmigaMidiRec/tree/main/Amiga_Boot_Disk (Amiga client, start this first)<br>
and https://github.com/wertstahl/AmigaMidiRec/tree/main/Send_Script_PY3 (drag any file on this on your system after you have installed all the periquisites)<br>
<br>
Party like it's 1992!<br>
