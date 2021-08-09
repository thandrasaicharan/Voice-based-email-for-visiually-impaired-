import  speech_recognition as sr #giving an alias name as sr just to make simple
import webbrowser as wb #giving the alias name as wb
import os
import pyttsx3 as py
import win32api
def load():
    global r,l,drives,list
    r=sr.Recognizer()
    drives = win32api.GetLogicalDriveStrings() #take a pick " 'C:\\\x00D:\\\x00' "
    drives = drives.split('\000')[:-1]
    l=[i[0] for i in  drives]
    #print(l)
    list=''
    for i in l:
        list+=i+', '
    #print(list)
def listening():
    global txt
    txt=''

    with sr.Microphone() as source:
        try:
            audio=r.listen(source,phrase_time_limit=3)
            txt=r.recognize_google(audio)
            txt = str(txt)
            print('you said :',txt)
            return txt
        except sr.UnknownValueError:
            py.speak('speech not recognized. please say again')
            listening()
def speaks():
    print('please select a choice.\n option a: search in internet.\n option b: open drives in the system.')
    while True:
        py.speak('please select a choice. option a. search in internet. option b. open drives in the system. please say your option.')
        result=listening()
        if result!=None:
            result=str(result).split()
            #print(result)
            if 'a' in result or 'A' in result:
            #if result in ['1',' option 1','1 option','search in internet']:
                print('please say a query to search:')
                py.speak('please say a query to search')
                print('listening')
                result=listening()
                wb.open(result)
                py.speak('check these results')
                activiate()
                break
            elif 'b' in result or 'B' in result or 'PNB' in result or 'HNB' in result :
                global drives
                x=''
            #elif result in ['2',' option 2','2 option','open drives','open drives in system']:
                while True:
                    txt='System has '+list+' drives. Which drive you want to open. say the open followed by drive name'
                    py.speak(txt)
                    result=listening()
                    print(result)
                    result=result.split()
                    # print(result)
                    # print(l)

                    for i in result:
                        for j in drives:
                            if j[0][0]==i:
                                x=j

                    if x in drives:
                        txt='opening '+x+' drive'
                        py.speak(txt)
                        os.startfile(x)
                        activiate()
                        break
                    else:
                        py.speak('the specified drive is not present in the system')
                break
            else:
                continue
        else:
            py.speak('Unknown error occured. Try again')


def activiate():
    py.speak('you can activate me again by saying. python')
    with sr.Microphone() as source:
        txt=''
        while txt!='python':
            try:
                audio=r.listen(source,phrase_time_limit=2)
                txt=r.recognize_google(audio)
                txt=str(txt).lower()
            except sr.UnknownValueError:
                continue
    py.speak('activated')





