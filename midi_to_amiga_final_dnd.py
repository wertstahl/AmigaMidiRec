import rtmidi
import os
import time
import sys
import msvcrt  # for Windows key press detection
import mouse   # for mouse click detection (requires 'mouse' module)

# === CHECK FILE ARGUMENT ===
if len(sys.argv) < 2:
    print("Usage: Drag and drop a file onto this script or run it with a file path.")
    sys.exit()

FILE_PATH = sys.argv[1]

if not os.path.isfile(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    sys.exit()



def dos_8_3(filename):
    # Get base name (without path)
    base = os.path.basename(filename)

    # Split into name and extension
    name, ext = os.path.splitext(base)

    # Remove leading dot from extension and make uppercase
    name = name.upper()[:16]
    ext = ext.upper().lstrip('.')[:3]

    if ext:
        return f"{name}.{ext}"
    else:
        return name


# Format filename for transfer
FCASE = dos_8_3(FILE_PATH)
print(FCASE)

# Evaluate MIDI devices
midi_out = rtmidi.MidiOut()
ports = midi_out.get_ports()
if not ports:
    print("No MIDI output ports found.")
    exit()

print("Available MIDI output ports:")
for i, port in enumerate(ports):
    print(f"{i}: {port}")

selected = input("Please select MIDI device by number: ")
try:
    selected_index = int(selected)
    midi_out.open_port(selected_index)
except:
    print("Invalid selection.")
    exit()

print(f"Filename will be: {FCASE} ...")
    
input("Press ENTER to start transfer.")

print(f"\nSending {FILE_PATH} once via MIDI. Press ESC to cancel.\n")


# Send header message
file_path_bytes = [ord(c) for c in FCASE]
header_sysex = [0xF0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, #give it some head start with 00 bytes
                0xF0, 0xEA] #our actual header bytes
midi_out.send_message(header_sysex)
#print("Header bytes sent.")
time.sleep(0.125)  # 125 ms pause 

filename_sysex =[0xF0] + file_path_bytes + [0xF0, 0xEA]
midi_out.send_message(filename_sysex)
print("Filename sent.")
time.sleep(0.125)  # 125 ms pause 



# Read file content
try:
    with open(FILE_PATH, "rb") as f:
        data = list(f.read())
except FileNotFoundError:
    print(f"File '{FILE_PATH}' not found.")
    exit()

# Function to send data in SysEx-compatible chunks (= 240 bytes of payload)
def send_sysex_chunks(midi_out, data, chunk_size=242):

    count = 0 # Counter for chunk hashes

    for i in range(0, len(data), chunk_size):
        if msvcrt.kbhit() and ord(msvcrt.getch()) == 27:
            print("Cancelled by ESC key.")
            sysex_msg = [0xF0 , 0xFF , 0xFF , 0xFF ]
            midi_out.send_message(sysex_msg)
            time.sleep(2)
            return

        chunk = data[i:i+chunk_size]
        sysex_msg = [0xF0] + chunk 
        midi_out.send_message(sysex_msg)
        time.sleep(0.015)  # 15 ms pause between chunks

        print("#", end="", flush=True) #print chunk hash
        count += 1
        if count % 64 == 0:
            print()  # Print newline after every 64 hashes

# Send data only once
try:
    send_sysex_chunks(midi_out, data)
except KeyboardInterrupt:
    print("Cancelled by keyboard interrupt.")

print("\nTransfer complete (or cancelled).")
midi_out.close_port()
time.sleep(2)
