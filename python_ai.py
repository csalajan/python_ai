from time import sleep
import pyaudio
import audioop
import wave
from pygsr import Pygsr
import wolframalpha
import urllib, urllib2, os
from chatterbot import (
        ChatterBotFactory as CBFactory, 
        ChatterBotType as CBType,
    )
from subprocess import Popen
 
class Record():
 
    def __init__(self):
        self.threshold = 26000
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

    def custom(self, query):
        ret = False
        #play music
        music = {"play music", "tunes", "jam", "play some music"}
        for x in music:
            if x in query:
                os.system("banshee --play &")
                ret = True
                return "Playing Music"

        #Stop Music
        music_stop = {"stop music", "quiet"}
        for x in music_stop:
            if x in query:
                os.system("banshee --stop &")
                ret = True
                return "Stopping Music"
        # EXIT BRUHH
        exit = ['exit', 'duck you', 'fellow']
        for x in exit:
            if x in query:
                return 'exit'

        if ret == False:
            return False

    
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
        else:
            return False
    
    def cleverbot(self, query):
        factory = CBFactory()
        bot1 = factory.create(CBType.CLEVERBOT)
        bot1session = bot1.create_session()

        return bot1session.think(query)


    def tts(self, query):
        url = "http://translate.google.com/translate_tts?tl=en&"
        parameters = {'q' : query}
        data = urllib.urlencode(parameters)
        url = "%s%s" % (url,data)
        return url

    def breakdown(self, query):
        tosay = []
        punct = [',',':',';','.','?','!'] #punctionation
        words = query.split(' ')
        sentence = ''
        for w in words:
            if w[len(w)-1] in punct: #encounter punctuation
                if (len(sentence)+len(w)+1<100): #is there enough space?
                    sentence += ' '+w #add word
                    tosay.append(sentence.strip()) #save teh sentence
                else:
                    tosay.append(sentence.strip())
                    tosay.append(w.strip())
                    sentence = ''
            else:
                if (len(sentence)+len(w)+1 < 100):
                    sentence += ' '+w
                else:
                    tosay.append(sentence.strip())
                    sentence = w
        if len(sentence) > 0:
            tosay.append(sentence.strip())
        return tosay

    def speak(self, query):
        toSay = self.breakdown(query)
        for sent in toSay:
            googleSpeechUrl = self.tts(sent)
            #agent = ("Mozilla/5.0 (Windows NT 6.1; WOW65) "
            #         "AppleWebKit/537.17 "
            #         "(KHTML, like Gecko) Chrome/25.0.1312.60 Safari/537.12")
            request = urllib2.Request(googleSpeechUrl)
            request.add_header('User-agent', 'Mozilla/5.0')
            opener = urllib2.build_opener()
            f = open("data.mp3", "wb")
            f.write(opener.open(request).read())
            f.close()
	    Popen(['mplayer', 'data.mp3', '-really-quiet']).wait()
            #os.system('mplayer -ao alsa -noconsolecontrols data.mp3')

if __name__ == '__main__':
    x = Record()
    x.setup()
    recorded = False
    response = None
    while response is not 'exit':
        x.read()
        rms = audioop.rms(x.data, 2)
        print rms
        if rms > x.threshold:
            speech = Pygsr()
            speech.record(5)
            phrase, complete_response = speech.speech_to_text('en_EN')
            response = x.custom(phrase)
            if response == False:
                response = x.Wolfram(phrase)
                if response == False:
                    response = x.cleverbot(phrase)
            print('PHRASEPHRASEPHRASE')
            print(phrase)
            print(response)
            x.speak(response)
            recorded = True
            rms = 0
        x.setup()
            

