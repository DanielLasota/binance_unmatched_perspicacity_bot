import threading
import pyaudio
import wave

class Winamp(threading.Thread):
    
    keygen_song_1 = 'Disease - Beautiful insanity.wav'
    
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        
    def run(self):
        wf = wave.open(self.filename, 'rb')

        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(1024)

        while data:
            stream.write(data)
            data = wf.readframes(1024)

        stream.stop_stream()
        stream.close()
        p.terminate()