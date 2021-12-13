import pyttsx3
from pywhatkit.mail import send_hmail 
import speech_recognition as sr    
import datetime      
import os     
import cv2
import random
import wikipedia    
from requests import get
import webbrowser
import pywhatkit as kit
import smtplib
import sys
import pyjokes
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import QTimer,QTime,QDate,Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from javis import Ui_MainWindow


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)
engine.setProperty('rate',10)


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def wish():
        hour =int(datetime.datetime.now().hour)
        if hour>=8 and hour<=12:
            speak("good morning")
        elif hour>12 and hour<18:
            speak("good afternoon")
        else:
            speak("good evening")
        speak("Hello, How can i help you")

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('hs9450331@gmail.com','mailpassword')
    server.sendmail("hs9450331@gmail.com",to,content)
    server.close

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.TaskExecution()
 
    def takecommand(self):
        r=sr.Recognizer()
        with sr.Microphone() as source:
            print('listening...')
            r.pause_threshold = 1
            audio = r.listen(source,timeout=1,phrase_time_limit=5)

        try:
            print("Recognizing")
            query = r.recognize_google(audio,language='en-in')
            print(f"user said {query}")
        except Exception as e:
            speak("say again")
            return "none"
        return query

    def TaskExecution(self):
        wish()
        while True:
            self.query = self.takecommand().lower()

            if "open notepad" in self.query:
                npath = "C:\\Windows\\System32\\notepad.exe"
                os.startfile(npath)
            elif "close notepad" in query:
                speak("closing notepad")
                os.system("taskkill /f /im notepad.exe") 

            elif "hide files" in self.query or "hide folder" in self.query or "visiable for everyone"in self.query:
                speak("tell me what you want to hide or make it visible")
                condition = self.takecommand().lower()
                if "hide" in condition:
                    os.system("attrib +h /s /d")
                    speak("The files or folder are hidden")
                elif "visible" in condition:
                    os.system("All files or folder are visible")

                elif "leave it" in condition or "leave for now" in condition:
                    speak("ok")

            elif " shutdown"in self.query:
                os.system("shutdown /s /t 5")

            elif "restart"in self.query:
                os.system("shutdown /r /t 5")

            elif "sleep" in self.query:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

            
            elif "open cmd"in self.query:
                os.system("start cmd")

            elif "open camera" in self.query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret,img=cap.read()
                    cv2.imshow('webcam',img)
                    k= cv2.waitKey(50)
                    if k==27:
                        break
                    cap.realease()
                    cv2.destroyAllWindows()
            elif "play music"in query:
                music_dir = "E:\\songs"
                songs = os.listdir(music_dir)
                rd = random.choice(songs)
                os.startfile(os.path.join(music_dir,rd))

            elif "wikipedia" in self.query:
                speak("searching wikipedia...")
                query = query.replace("wikipedia","")
                results = wikipedia.summary(query,sentences = 2)
                speak("according to wikipedia")
                speak(results)
            elif "open youtube" in self.query:
                webbrowser.open("www.youtube.com")
            elif "joke" in self.query():
                joke = pyjokes.get_joke()
                speak(joke)

            elif "open facebook" in self.query:
                webbrowser.open("www.facebook.com")
            elif "open insta" in query:
                webbrowser.open("www.instagram.com")

            elif "open google" in self.query:
                speak("what should i search on google ")
                cm = self.takecommand().lower()
                webbrowser.open(f"{cm}")

            elif "send message" in self.query:
                kit.sendwhatmsg("+918398945887","this is for testing",8,35)

            elif "email" in self.query:
                try:
                    speak("what should i send?")
                    content = self.takecommand().lower()
                    to="himanshu.sharmav45@gmail.com"
                    sendEmail(to,content)
                    speak("Email has been sent")
                except Exception as e:
                    print(e)
                    speak("mail not send")
            elif "new"in self.query():
                speak("News Feteching")

            elif "no thanks"in self.query:
                speak("Thanks for using")
                sys.exit()


            speak("Anything you want to search")

startExecution = MainThread()
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("C:/Users/sagar sharma/Downloads/7LP8.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C:/Users/sagar sharma/Downloads/Jarvis_Loading_Screen.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())




