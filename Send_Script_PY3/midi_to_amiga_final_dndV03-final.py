#!/usr/bin/env python3
# midi_to_amiga_final_dnd.py
# PC -> Amiga raw MIDI sender (custom F0-prefixed framing)
# (c)5/2025, 9/2025 by Sebastian I. Hartmann
# Use at your own risk.
#
# - Header burst
# - Filename (ASCII, framed)
# - Total chunk count (16 ASCII digits, framed)
# - Data streamed in [F0]+payload chunks with 15 ms gaps
#
# Requires: python-rtmidi
#   pip install python-rtmidi

import sys
import os
import time
import atexit

def _wait_for_space_to_exit():
    try:
        # Don't block if not attached to a real console
        if not sys.stdout.isatty():
            return
        print("\nPress SPACE to exit...", end="", flush=True)
        if os.name == "nt":
            import msvcrt
            while True:
                ch = msvcrt.getch()
                if ch in (b' ',):
                    break
        else:
            # Fallback: just hit Enter on non-Windows
            input()
    except Exception:
        # Never let shutdown be blocked by an error here
        pass

atexit.register(_wait_for_space_to_exit)


# Optional Windows-only ESC detection
try:
    import msvcrt  # noqa: F401
    _HAS_MSVCRT = True
except Exception:
    _HAS_MSVCRT = False

try:
    import rtmidi
except ImportError:
    print("This script needs python-rtmidi. Install with:  pip install python-rtmidi")
    sys.exit(1)

# -----------------------------
# Config
# -----------------------------
CHUNK_SIZE = 242            # payload bytes per frame
CHUNK_GAP_SEC = 0.015       # 15 ms between frames
POST_FILENAME_PAUSE = 0.125 # short settle before streaming
COUNT_DIGITS_SENT = 16      # digits sent to Amiga (per your current receiver)
COUNT_DIGITS_PRINT = 8      # digits shown in progress line


# -----------------------------
# Helpers
# -----------------------------

def sanitize_name(stem: str) -> str:
    """
    Upper-case, strip disallowed chars, and trim to 16 chars.
    """
    allowed = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
    s = "".join((c if c in allowed else "_") for c in stem.upper())
    return s[:16] if len(s) > 16 else s

def build_transfer_name(path: str) -> str:
    """
    Build the transfer name similar to a relaxed 8.3:
    - stem up to 16 upper-case safe chars
    - ext up to 3 upper-case chars (optional)
    """
    base = os.path.basename(path)
    stem, ext = os.path.splitext(base)
    stem = sanitize_name(stem)
    ext = ext[1:].upper()[:3] if ext else ""
    return f"{stem}.{ext}" if ext else stem

def choose_midi_port(midi_out: "rtmidi.MidiOut"):
    ports = midi_out.get_ports()
    if not ports:
        print("No MIDI output ports found.")
        sys.exit(1)
       
    print("\nAvailable MIDI outputs:")
    for i, p in enumerate(ports):
        print(f"  [{i}] {p}")
    while True:
        sel = input(f"Select port [0..{len(ports)-1}]: ").strip()
        if sel == "":
            sel = "0"
        if sel.isdigit() and 0 <= int(sel) < len(ports):
            idx = int(sel)
            return idx, ports[idx]     # return name now so we don't re-enumerate later
        print("Invalid selection. Try again.")

def send_header_burst(midi_out: "rtmidi.MidiOut"):
    # Matches your Amiga-side expectation:
    # [F0, 00,00,00,00,00,00, F0, EA]
    msg = [0xF0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xF0, 0xEA]
    midi_out.send_message(msg)

def send_framed_ascii(midi_out: "rtmidi.MidiOut", text: str):
    # Frame: [F0] + ASCII bytes + [F0, EA]
    payload = [0xF0] + [ord(c) for c in text] + [0xF0, 0xEA]
    midi_out.send_message(payload)

def send_chunk_count(midi_out: "rtmidi.MidiOut", total_chunks: int):
    # Send as 16 ASCII digits, zero-padded
    s = f"{total_chunks:0{COUNT_DIGITS_SENT}d}"
    send_framed_ascii(midi_out, s)
    #print(f"Total chunks sent to Amiga: {s}", flush=True)

def esc_pressed() -> bool:
    if not _HAS_MSVCRT:
        return False
    if msvcrt.kbhit():
        ch = msvcrt.getch()
        try:
            code = ch[0] if isinstance(ch, (bytes, bytearray)) else ord(ch)
        except Exception:
            code = None
        return code == 27
    return False

def send_cancel(midi_out: "rtmidi.MidiOut"):
    # Custom cancel burst, then give the Amiga a moment
    midi_out.send_message([0xF0, 0xFF, 0xFF, 0xFF])
    time.sleep(2.0)

def send_data_stream(midi_out: "rtmidi.MidiOut", data: bytes, total_chunks: int):
    sent = 0
    # In-place single-line progress
    while sent < len(data):
        if esc_pressed():
            print("\nCancelled by ESC key.")
            send_cancel(midi_out)
            return False
        chunk = data[sent:sent + CHUNK_SIZE]
        midi_out.send_message([0xF0] + list(chunk))
        sent += len(chunk)
        done_chunks = (sent + CHUNK_SIZE - 1) // CHUNK_SIZE
        print(
            f"\rTransmitting total chunks {total_chunks}  current: {done_chunks}",
            end="",
            flush=True
        )
        time.sleep(CHUNK_GAP_SEC)
    print()  # newline
    return True


# -----------------------------
# Main
# -----------------------------

def main():
    if len(sys.argv) < 2:
        print("Drag-and-drop a file onto this script or pass a path as an argument.")
        path = input("File to send: ").strip().strip('"')
        if not path:
            return
    else:
        path = sys.argv[1]

    if not os.path.isfile(path):
        print(f"Not a file: {path}")
        return

    # Read the data once
    with open(path, "rb") as f:
        data = f.read()

    # Compute chunk count and formatted strings
    total_chunks = (len(data) + CHUNK_SIZE - 1) // CHUNK_SIZE
    total_chunks_print = min(total_chunks, 10**COUNT_DIGITS_PRINT - 1)

    # Build transfer name
    xfer_name = build_transfer_name(path)
    print("-----------------------------------------------------")
    print("Midi To Amiga Data transfer aka MidiRec v0.3 - 9/2025")
    print("(c) Sebastian I. Hartmann 2025 - Use at your own risk")
    print("-----------------------------------------------------")
    print("Attention: this is a one-way no feedback-transfer.   ")
    print("You may drag and hide this window, but make sure     ")
    print("to not delay serial transfer (avoid CPU spikes).     ")
    print("Always check the integrity of the data after sending.")
    print("We just send, no confirmations, no talkback.         ")
    print("-----------------------------------------------------")
    
    print(f"\nTransfer name: {xfer_name}")
    print(f"File size: {len(data)} bytes")
    print(f"Chunk size: {CHUNK_SIZE}  -> total chunks: {total_chunks}")

    # MIDI setup
    midi_out = rtmidi.MidiOut()
    port_index, port_name = choose_midi_port(midi_out)
    print(f"Opening: {port_name}", flush=True)
    midi_out.open_port(port_index)
    print("Opened OK.", flush=True)

    try:
        # Header
        print("Sending header...", flush=True)
        send_header_burst(midi_out)
        time.sleep(0.05)
        print("Header sent.", flush=True)
        t0 = time.perf_counter()

        # Filename
        print("Sending filename...", flush=True)
        send_framed_ascii(midi_out, xfer_name)
        print("Filename sent.", flush=True)
        time.sleep(POST_FILENAME_PAUSE)

        # Total chunk count (16 ASCII digits)
        print("Sending total chunk count...", flush=True)
        send_chunk_count(midi_out, total_chunks)

        # Stream data
        ok = send_data_stream(midi_out, data, total_chunks_print)
        if ok:
            print("Transfer complete.")
        else:
            print("Transfer aborted.")

        elapsed = time.perf_counter() - t0
        mins, secs = divmod(elapsed, 60)
        print(f"Elapsed: {elapsed:.2f} s  ({int(mins)} min {secs:.2f} s)")
    
    except KeyboardInterrupt:
        print("\nCancelled by keyboard interrupt.")
        send_cancel(midi_out)
    finally:
        try:
            midi_out.close_port()
        except Exception:
            pass

if __name__ == "__main__":
    main()
