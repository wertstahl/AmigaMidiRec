<b>AmigaMidiRec - Transfer File from any OS to Amiga via MIDI -- easy drag and drop</b><br>
<br>
<b>#INFO:</b> This transfer method is slow but uses very affordable components. It is slow<br>
because MIDI transfer is hardwired to 1983 standards:<br>
Midi is fixed to 31520 Bauds. 31,250 bits per second (31.25 kbit/s) minus some pause every 242 bytes.<br>
https://en.wikipedia.org/wiki/MIDI <br>
<br>
<br>
<b>#USECASE:</b> <i>you need to have <green><b>that file</b></green> sent over to the Amiga, and you have MIDI.<br> 
You do not want to swap floppies, you don't want or cannot use floppies or any other connection to the Amiga.</i><br>
<br>
<br>
<b>#DISCLAIMER: This is experimental software, use at your own risk. Files in the Amiga RAM: Disk will be<br>
overwritten without asking (not a big deal). This is just a for-fun project, but it can be pretty helpful.<br>
And it is faster with <500kb files, than writing a floppydisk on your PC and then reading that floppydisk on the Amiga.<br>
! Warning: 1.6 MB take about 15 Minutes, just so you have been informed. <br>
<br></b>
<b>#HOWTO:</b><br>
1. On the Amiga side make sure you have enough RAM. Like 2 MB and more. <br>
2. <b>! Somehow you manage to get MidiRecieveToRam.exe onto a Workbench 1.3+ boot disk with serial.device <br>
   to work on your Amiga - perhaps just write the included DMS to a floppy and boot from that.  </b> <br>
   Just copying the file to the disk won't do, you'll need DMS <br>
   (use UAE or https://www.aminet.net/package/util/arc/dmsgui18 and https://www.aminet.net/package/util/arc/dms111)<br>
   DirOpus (Dopus) should also be able to write DMS images to Floppydisk.<br>
   If you have a pre Windows 7 PC with floppy drive, maybe Omniflop can do the job:<br>
   https://www.youtube.com/watch?v=F7fSqi6QCyQ<br> 
   http://www.shlock.co.uk/Utils/OmniFlop/OmniFlop.htm<br>
3. On the Amiga you start MidiRecieveToRam.exe  - and on your Amiga you also have<br>
   <b>a Midi interface that connects your Amiga MIDI IN <-- to your PC MIDI OUT --> </b>
4. Over on your PC you drag and drop any file you want to send to the Amiga on the python script midi_to_amiga_final_dnd.py<br>
5. Select your Midi output device on the PC side, confirm, and ... wait for quite some time ...<br>
6. Amiga side should show file name confirmatin and # chunk progress.<br>
7. With very lowered expectations wait for everything to unfold, it will take alot of time (15 minutes for 1,6 MB)<br>
8. When done, check your Amiga RAM: disk, file will be there. Test it! There is no error correction.<br>
9. Again: this is experimental software just for the fun of it. Use at your own risk.<br>
10. Don't use this software if you don't know what you're doing, no shirt, no shoes, no support.<br>
11. Modify all the parameters to your preferences, maybe increasing the sleep in line 117 of the py script to 0.125 helps.<br>
12. midi_to_amiga_final_dnd.py is a Python 3 Script that requires:<br>
<br>
<b>#<i>(any OS) PC Side></i> PRERIQUISITES:<br>
Python: https://www.python.org/downloads/ --> 3.10<br>
also <b>pip install</b>: <br>
rtmidi<br>
os<br>
time<br>
sys<br>
msvcrt  (perhaps only on Windows PCs) <br>
mouse<br>
<br>
If you like to code: Amiga Blitz Basic2: https://archive.org/details/ultimate-blitz-basic-v2_1<br>
with this you can modify the Amiga (receiver side) to your preference.<br>
<br>
<br>
<b>AUTHOR:</b> (c)6/2025 by S.I.Hartmann aka WS (ex G*P), based on code by Claude Heiland-Allen https://mathr.co.uk/amiga/<br>
<br>
NOTE: this was only tested on real hardware. No idea if a loopback from WINUAE to local OS actually works. If you had any success with that, let me know.<br>
<br>
<b>QUICK START: The files you would most likely want to try out are:<br>
https://github.com/wertstahl/AmigaMidiRec/blob/main/Amiga_Boot_Disk/MIDIGETWB13.DMS<br>
(Amiga client, write this to an Amiga Floppy, boot from it and start the executable <i>MidiRecieveToRam.exe</i> first<br>
- have your Midi cables connected from PC-->Midi-out to Amiga-->Midi-in !)<br>
and https://github.com/wertstahl/AmigaMidiRec/blob/main/Send_Script_PY3/midi_to_amiga_final_dnd.py<br>
(drag and drop any file on this on your system after you have installed all the periquisites<br>
and only after starting the client on your Amiga)<br>
</b><br>
Party like it's 1992!<br>
