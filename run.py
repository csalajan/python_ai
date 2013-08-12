#import cli.app
import wolframalpha
#from chatterbot import ChatterBotFactory, ChatterBotType
import pyaudio
import audioop
 
chunk = 1024
  
p = pyaudio.PyAudio()
   
stream = p.open(format=pyaudio.paInt16,
    channels=1,
    rate=44100,
    input=True,
    frames_per_buffer=chunk)
    
def test():
    while True:
        data = stream.read(chunk)
        rms = audioop.rms(data, 2)
        if rms > 17000:
            print(rms)
        
test()
def Wolfram(query):
    wolfram_id='6XRJP6-E45RHG32RR'
    client = wolframalpha.Client(wolfram_id)
    res = client.query(query)
    if len(res.pods)  > 0:
        texts = ""
        pod = res.pod[1]
        if pod.text:
            texts = pod.text
        else:
            return "I do not have an answer for that"
        texts = texts.encode('ascii', 'ignore')
        return texts

def Cleverbot(query):
    factory = ChatterBotFactory()
    bot1 = factory.create(ChatterBotType.CLEVERBOT)
    bot1session = bot1.create_session()

    return bot1session.think(query)

