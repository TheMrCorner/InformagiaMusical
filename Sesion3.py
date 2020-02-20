# Sesion 3 de laboratorio, testeando cosas
import pyaudio, wave, kbhit

#Abriendo archivos de audio
wf = wave.open('fray.wav', 'rb')

# Lectura de pulsaciones de teclado
kb = kbhit.KBHit()

# Instancia de PyAudio
p = pyaudio.PyAudio()

print("Hello There!")

# Stream
stream = p.open(
    format=p.get_format_from_width(wf.getsampwidth()),
    channels=wf.getnchannels(),
    rate=wf.getframerate(),
    output=True)

CHUNK = 1024

# Leemos los datos del wav
data = wf.readframes(CHUNK)

c = ' '
while c != 'q':
    if kb.kbhit():
        c = kb.getch()
        print("Tecla pulsada: ", c)

kb.set_normal_term()

# Escribimos en stream, esto es bloqueante
cont = 1
while len(data) > 0:
    print("Reproduciendo chunk: ", cont)
    stream.write(data)
    data = wf.readframes(CHUNK)
    cont = cont + 1

# Finalizamos el stream
stream.stop_stream()
stream.close()

# finalizamos
p.terminate()