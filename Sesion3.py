# Laboratory Sesions 3-4
import pyaudio, kbhit
import numpy as np  # Arrays
from scipy.io import wavfile  # wav management

# Global variables
CHUNK = 1024 # Buffer size

# Cargamos el archivo wav en la variable data
SRATE, data = wavfile.read('song.wav')

# Check de formato de samples
if data.dtype == 'int16':      formt = 2
elif data.dtype == 'int32':    formt = 4
elif data.dtype == 'float32':  formt = 4
elif data.dtype == 'uint8':    formt = 1
else: raise Exception('Data format not supported')

# Prepare PyAudio
# Init and create instance
p = pyaudio.PyAudio()

block = np.arange(CHUNK, dtype=data.dtype)  # Array

# Defining callbacks
def callback (in_data, frame_count, time_info, status):
    # frame_count: number of frames to return
    # frame_count = CHUNK
    global numBlocks = 0
    print ("Callback bloque ", numBlocks, "fc: ", frame_count)

    # Block's array
    block = data [numBlocks*CHUNK : numBlocks*CHUNK+CHUNK]
    numBlocks += 1

    # Return block
    return (block, pyaudio.paContinue)

# Stream
stream = p.open(
    format=p.get_format_from_width(formt),   # Sample format
    channels=len(data.shape),                # Channels
    rate=SRATE,                              # Frecuency
    frames_per_buffer=CHUNK,                 # Buffer size
    output=True)                             # Stream output

# Keyboard reading
kb = kbhit.KBHit()

# Testing keyboard reading
# c = ' '
# while c != 'q':
#     if kb.kbhit():
#         c = kb.getch()
#         print("Tecla pulsada: ", c)

# Processing each chunk of sound
numBlocks = 0                                # Counter
char = ' '
vol = 1.0
while char != 'q':
    # new block

    # Volume modification
    block = block*vol

    # write on stream converting type
    stream.write(block.astype((data.dtype)).tobytes())

    if kb.kbhit():
        char = kb.getch()
        if (char == 'v'): 
            vol = max(0, vol-0.05)
        elif (char == 'V'): 
            vol = min(1, vol+0.05)
        print("Vol: ", vol)

    numBlocks += 1

# Write on the stream, this blocks the program
# cont = 1
# while len(data) > 0:
#     print("Reproduciendo chunk: ", cont)
#     stream.write(data)
#     data = wf.readframes(CHUNK)
#     cont = cont + 1

# Ending and stopping kbhit
kb.set_normal_term()

# Stopping and ending stream
stream.stop_stream()
stream.close()

# Ending program
p.terminate()