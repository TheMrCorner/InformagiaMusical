import pyaudio, kbhit
import numpy as np  # Arrays
from scipy.io import wavfile  # wav management

# Variables globales
RATE = 44100
CHUNK = 1024

formt = 4

# Prepare PyAudio
# Init and create instance
p = pyaudio.PyAudio()

# Stream
stream = p.open(
    format=p.get_format_from_width(formt),   # Sample format
    channels=1,              # Channels
    rate=RATE,                              # Frecuency
    frames_per_buffer=CHUNK,                 # Buffer size
    output=True) 
    
# Keyboard reading
kb = kbhit.KBHit()

def osc(frec, vol, frame):
    return vol*np.sin(2*np.pi*(np.arange(CHUNK)+frame)*frec/RATE)


frec = 440 # Nota

vols = [0.3, 0.2, 0.15, 0.15, 0.1, 0.1]

frame = 0

while True:
    arms = [frec*(i+1) for i in range(len(vols))]

    samples = np.zeros(CHUNK, dtype=np.float32)

    frame = frame + CHUNK

    for i in range(len(vols)):
        samples = samples + osc(arms[i], vols[i], frame)

    stream.write(samples.astype(np.float32))

# Stopping and ending stream
stream.stop_stream()
stream.close()

# Ending program
p.terminate()