from VoiceGmail import *
from smartcomputer import *

print('Welcome User')
print('option a: voice based mailing system')
print('option b: smart system')
print('option c: Exit')
py.speak('Welcome user. which operation u want to perform.')
value=''
def listeningM():
    global value
    value=''
    with sr.Microphone() as source:
        try:
            audio=r.listen(source,phrase_time_limit=3)
            txt=r.recognize_google(audio)
            txt = str(txt)
            print('you said :',txt)
            value=txt
            return value
        except sr.UnknownValueError:
            py.speak('speech not recognized. please say again')
            listeningM()

def start():
    while True:
        #value=''
        py.speak(' option a. voice based mail system. option b. smart system. option c. exit.')
        py.speak('please say an option')
        result=listeningM()
        #print(result)
        if result!=None:
            result=result.split()
           #print(result)
            if 'A' in result or 'a' in result or 'TNA' in result: #result in [' option 1','1','1 option']:
                welcome()
            elif 'B' in result or 'b' in result or 'PNB' in result or 'HNB' in result: #result in ['option 2','2','2 option']:
                speaks()
            elif 'c' in result or 'C' in result or 'exit' in result or 'Exit' in result: #result in [' option 3','3','3 option']:
                py.speak('closing the application')
                break
            else:
                py.speak('please select a valid option')
        else:
            py.speak('Unknow Error occured. Trying again')
    exit(0)

load()
start()
