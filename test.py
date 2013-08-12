import pyaudio
import audioop
import wave
from pygsr import Pygsr
import wolframalpha
 
class Record():
 
    def __init__(self):
        self.threshold = 17000
        self.format = pyaudio.paInt16
        self.chunk = 1024
        self.rate = 44100
        self.input = True
        self.frames_per_buffer = self.chunk
        self.record_seconds = 5
        self.file = 'hello.wav'
        self.channels = 2
        self.data = ''
 
    def setup(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=self.input,
                                  frames_per_buffer=self.frames_per_buffer)
     
    def close(self, p, stream):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        
    def record(self):
        print('recording...')
 
        self.frames = []
 
        rms = audioop.rms(self.data, 2)
        for i in range(0, int(self.rate/self.chunk*self.record_seconds)):
            self.data = self.stream.read(self.chunk)
            self.frames.append(self.data)
 
        print('done recording.')
 
    def save(self):
        wf = wave.open(self.file, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
 
    def read(self):
        self.data = self.stream.read(self.chunk)

    def Wolfram(self, query):
        wolfram_id='6XRJP6-E45RHG32RR'
        client = wolframalpha.Client(wolfram_id)
        res = client.query(query)
        if len(res.pods)  > 0:
            texts = ""
            pod = res.pods[1]
            if pod.text:
                texts = pod.text
            else:
                return "I do not have an answer for that"
            texts = texts.encode('ascii', 'ignore')
            return texts

if __name__ == '__main__':
    x = Record()
    x.setup()
    recorded = False
    while not recorded:
        x.read()
        rms = audioop.rms(x.data, 2)
        if rms > x.threshold:
           # x.record()
           # x.save()
           # recorded = True
           # x.stt()
           speech = Pygsr()
           speech.record(5)
           phrase, complete_response = speech.speech_to_text('en_EN')
           response = x.Wolfram(phrase)
           print(response)
           recorded = True
