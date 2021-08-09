import imaplib
import email
import pyttsx3 as py
import speech_recognition as sr
import smtplib
r=sr.Recognizer()

#function to load the required varibles
def loadVariables():
    global email_id,password



#function for readmails
def seenMails(mail):
    mail.select()
    return_code2, dataSeen = mail.search(None,'Seen')
    mail_ids_seen = dataSeen[0].decode()
    id_list_seen = mail_ids_seen.split()
    if len(id_list_seen):
        print('read mails are', len(id_list_seen))
    else:
        print('No read message')
    return mail,id_list_seen

#function for unread mails
def unseenMails(mail):
    mail.select()
    return_code, dataUnseen = mail.search(None, 'UnSeen')
    mail_ids_unseen = dataUnseen[0].decode()
    id_list_unseen = mail_ids_unseen.split()
    if len(id_list_unseen):
        print('unseen mails are',len(id_list_unseen))
    else:
        print('No unseen mails are present')
    return mail,id_list_unseen

#fuction for view the mails
def viewMail(mail,data,txt):
    last_range=int(data[-1])+1
    for i in range(int(data[0]),int(data[-1])+1):
        result=''
        typ, data = mail.fetch(str(i), '(RFC822)') #include in documnet,UTF-8 is a variable-width character encoding used for electronic communication
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1].decode("utf-8"))
                email_subject = msg['subject']
                email_from = msg['from']
                body = msg.get_payload()
                body = str(body[0]).split('\n')
                result=speakMail(str(email_subject),str(email_from),str(body[2]),str(i))
        if result:
            if i==last_range:
                txt='all '+txt+' are completed'
                py.speak(txt)
            else:
                continue
        else:
            break

#questioning  function
def quAsk(message):
    t=message
    message='Do you want to read '+message+'. yes or no'
    with sr.Microphone() as source:
        py.speak(message)
        options = ['yes', 'Yes', 's', 'S']
        try:
            audio = r.listen(source,phrase_time_limit=3)
            txt = r.recognize_google(audio)
            if str(txt) in options:
                return True
            else:
                return False
        except sr.UnknownValueError:
            quAsk(t)

#function to speak the mails
def speakMail(email_subject,email_from,email_body,messgage_no):
    print('From:',email_from)
    print('Subject:',email_subject)
    print('Message:',email_body)
    while True:
        txt='From '+email_from+'.'+'Subject : '+email_subject+'.'+'message:'+email_body+'.'
        py.speak(txt)
        result=quAsk('mail again')
        if result:
            continue
        else:
            #result=mailMovement(messgage_no)
            result=quAsk('next mail')
            if result:
                return True
            else:
                return False



def getResponse(txt):
    options = ['yes', 'Yes', 's', 'S']
    with sr.Microphone() as source:
        py.speak(txt)
        try:
            audio=r.listen(source,phrase_time_limit=4)
            response=r.recognize_google(audio)
            response=str(response)
            print('your choice :',response)
            if response in options:
               return True
            else:
                return False
        except sr.UnknownValueError:
            py.speak('voice is not clear. say again.')
            getResponse(txt)
def getPassword(email_id_arg):
    global password,email_tmp,email_id
    email_tmp=email_id_arg
    with sr.Microphone() as source:
            text=''
            password=''
            print('please say you password :',end='')
            py.speak('Please say password')
            while text=='':
                audiop = r.listen(source,phrase_time_limit=4)
                text = (r.recognize_google(audiop))
                password= str(text).replace(" ", '')
                text = 'your password is,' + password
                py.speak(text)
                print(password)
            password=password
            #email_id='sendermail575@gmail.com'
           # password='sender123'
            txt='Do you want to proceed with this password. yes or no.'
            print(txt)
            result = getResponse(txt)
            if result == True:
                print(email_tmp,password)
                if email_tmp==None and password==None:
                    getPassword(email_tmp)
                else:
                    return email_tmp,password
            else :
                getPassword(email_tmp)

def getMailid(evalue,pvalue):
    global email_id,password
    print('Please say your mail id :', end='')
    py.speak('Please say your mail id')
    with sr.Microphone() as source:
        text=''
        while text == '':
            audio = r.listen(source,phrase_time_limit=10)
            text = (r.recognize_google(audio))
            email_id = str(text).replace(" ", '')
            if "@gmail.com" in email_id:
                pass
            else:
                email_id=email_id+"@gmail.com"
            print(email_id)
            text = 'your mail id is,' + email_id
            py.speak(text)
        txt='Do you want to proceed with this mail id. yes or no. '
        print(txt)
        result=getResponse(txt)
        if result==True:
            #email_id,password=getPassword(email_id)
            getPassword(email_id)
            print(email_id,password)
            #evalue=email_id
            #pvalue=password
            return email_id,password
        else:
            getMailid(evalue,pvalue)

#function to login into mail
def mailLogin():
    global email_id,mail,password
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    evalue=''
    pvalue=''
    #email_id,password=getMailid(evalue,pvalue)
    getMailid(evalue,pvalue)
    #print(email_id,password)
    try:
        mail.login(email_id, password)
        print('Login successful')
        py.speak('Login Successful')
        mail.select()
        return mail,email_id,password
    except imaplib.IMAP4.error:
        print('Invalid crendentials.\n login Failed')
        py.speak("Invalid crendentials. Login failed")
        return None,None,None
    except:
        print('unknowm problem occured please try again')
        py.speak('Authentication problem has  occured')
        return None,None,None

def getMessage(txt,limit=None,check=None):
    with sr.Microphone() as source:
        try:
            py.speak(txt)
            audio=r.listen(source,phrase_time_limit=limit)
            txt=r.recognize_google(audio)
            if check:
                txt=str(txt).replace(' ','')
            return txt
        except sr.UnknownValueError:
            getMessage(txt)

#function to send mail
def sendMail(email_id,password):
    mail=smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    try:
        mail.login(email_id,password)
        print('Receiver mail address:')
        reciver_mail=getMessage('please say the reciver mail address',limit=10,check=True)
        if '@gmail.com' in reciver_mail:
            pass
        else:
            reciver_mail=reciver_mail+'@gmail.com'
        print('TO :',reciver_mail)
        msg=getMessage('please say the message to send :')
        print('Message :',msg)
        mail.sendmail(email_id,reciver_mail,msg)
        py.speak('mail sent successfully')
        print('mail sent successfully')
        return True
    except:
        py.speak('Unknown error occured while sending mail. please try again')
        return

def welcome():
    print('Welcome to voice based mailing system')
    loadVariables()
    py.speak('Welcome to voice based mailing system')
    mail,email_id,password=mailLogin()
    if mail:
        while True:
            txt='please select your choice. option a. compose mail. option b. read mails. option c. exit.'
            print(txt)
            result=getMessage(txt,3)
            result=str(result).split()
            if 'a' in result or "A" in result:
                mail.logout()
                sendMail(email_id,password)
                mail = imaplib.IMAP4_SSL('imap.gmail.com')
                mail.login(email_id,password)
                mail.select()
            elif 'b' in result or 'B' in result:
                txt='please select choice. option a. seen mails. option b. unseen mails'
                print(txt)
                result=getMessage(txt,3)
                result = str(result).split()
                if 'a' in result or 'A' in result:
                    mail,no_of_seen_mails=seenMails(mail)
                    txt='you have '+str(len(no_of_seen_mails))+' mails.'
                    py.speak(txt)
                    if len(no_of_seen_mails):
                        viewMail(mail,no_of_seen_mails,'seen mails')
                if 'b' in result or 'B' in result:
                    mail,no_of_unseen_mails=unseenMails(mail)
                    txt='you have '+str(len(no_of_unseen_mails))+' mails'
                    py.speak(txt)
                    if len(no_of_unseen_mails):
                        viewMail(mail,no_of_unseen_mails,'unseen mails')
            elif 'c' in result or 'C' in result:
                print('you are exiting from voice based mail system application. Thank you')
                py.speak('you are exiting from voice based mail system application. Thank you')
                mail.logout()
                break
            else:
                continue
    else:
        return None


#mailLogin()