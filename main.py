import threading
import pyaudio
import wave
import os
from tkinter import *
from tkinter import filedialog
from lib.RecognitionLib import *

global filePath
global clf

path = "lib/trainedModel.sav"
clf = loadModel(path)
filePath = "unknow"


# Audio record

class App():
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100

    frames = []

    def __init__(self, master):

        self.isrecording = False
        self.button1 = Button(app, text='Recording', width=12, command=self.startrecording)
        self.button2 = Button(app, text='Stop Recording', width=12, command=self.stoprecording)
        self.button1.place(x=300, y=200)
        self.button2.place(x=400, y=200)

    def startrecording(self):

        textTest = "Please read this text for the record :"

        textTest1 = "In computer science, artificial intelligence, sometimes called machine intelligence,                         "
        textTest2 = "is intelligence demonstrated by machines, in contrast to the natural intelligence displayed                  "
        textTest3 = "by humans and animals. An intelligent agent is any device that perceives its environment                     "
        testText4 = "and takes actions that maximize its chance of successfully achieving its goals.                              "


        self.textParkiTest = Label(app, text=textTest, font=('bold', '13'), bg='red')
        self.textParkiTest.place(x=0, y=270)

        self.textParkiTest1 = Label(app, text=textTest1, font=('normal', '11'), bg='#facd54')
        self.textParkiTest1.place(x=0, y=300)
        self.textParkiTest2 = Label(app, text=textTest2, font=('normal', '11'), bg='#facd54')
        self.textParkiTest2.place(x=0, y=320)
        self.textParkiTest3 = Label(app, text=textTest3, font=('normal', '11'), bg='#facd54')
        self.textParkiTest3.place(x=0, y=340)
        self.textParkiTest4 = Label(app, text=testText4, font=('normal', '11'), bg='#facd54')
        self.textParkiTest4.place(x=0, y=360)

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.sample_format, channels=self.channels, rate=self.fs,
                                  frames_per_buffer=self.chunk, input=True)
        self.isrecording = True

        print('Recording')
        global t
        t = threading.Thread(target=self.record)
        t.start()

    def stoprecording(self):
        if self.isrecording == False:
            print("Press Recoring button first")
        else:
            self.textParkiTest.destroy()
            self.textParkiTest1.destroy()
            self.textParkiTest2.destroy()
            self.textParkiTest3.destroy()
            self.textParkiTest4.destroy()

            self.isrecording = False
            print('recording complete')
            self.filename = "recordingAudio.wav"
            wf = wave.open(self.filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.sample_format))
            wf.setframerate(self.fs)
            wf.writeframes(b''.join(self.frames))
            wf.close()

    def record(self):
        self.frames.clear()
        while self.isrecording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)


def chooseFile():
    global filePath
    filePath = filedialog.askopenfilename(initialdir="/C", title="Select a file", filetypes=[("wav file", "*.wav")])
    print("path :", filePath)


def execAI():
    global part_label1
    global part_label2
    global part_label3
    global filePath
    errmsg = "Path not valid"

    if ((filePath == "unknow") or (filePath == "")) and os.path.exists("recordingAudio.wav"):
        filePath = "recordingAudio.wav"

    if (filePath != "unknow") and (filePath != ""):
        if predict(clf, filePath):
            # Test label1
            try:
                part_label1
            except NameError:
                part_label1 = None

            if part_label1 is not None:
                part_label1.destroy()
            # Test label2
            try:
                part_label2
            except NameError:
                part_label2 = None

            if part_label2 is not None:
                part_label2.destroy()
            # Test label3
            try:
                part_label3
            except NameError:
                part_label3 = None

            if part_label3 is not None:
                part_label3.destroy()

            # Display answer
            part_label1 = Label(app, text='Yes', font=('bold', 14), bg='#facd54', pady=20)
            part_label1.place(x=400, y=105)
        else:
            # Test label1
            try:
                part_label1
            except NameError:
                part_label1 = None

            if part_label1 is not None:
                part_label1.destroy()
            # Test label2
            try:
                part_label2
            except NameError:
                part_label2 = None

            if part_label2 is not None:
                part_label2.destroy()
            # Test label3
            try:
                part_label3
            except NameError:
                part_label3 = None

            if part_label3 is not None:
                part_label3.destroy()

            # Display answer
            part_label2 = Label(app, text='No', font=('bold', 14), bg='#facd54', pady=20)
            part_label2.place(x=400, y=105)
        filePath = "unknow"
    else:
        # Test label1
        try:
            part_label1
        except NameError:
            part_label1 = None

        if part_label1 is not None:
            part_label1.destroy()
        # Test label2
        try:
            part_label2
        except NameError:
            part_label2 = None

        if part_label2 is not None:
            part_label2.destroy()
        #Test label3
        try:
            part_label3
        except NameError:
            part_label3 = None

        if part_label3 is not None:
            part_label3.destroy()

        # Display answer
        part_label3 = Label(app, text=errmsg, font=('bold', 14), bg='#facd54', pady=20)
        part_label3.place(x=400, y=105)

        print(errmsg)
        return errmsg
    if os.path.exists("recordingAudio.wav"):
        os.remove("recordingAudio.wav")


# Create Window
app = Tk()
app.resizable(False, False)

# background
filename = PhotoImage(file="img/bn3-bg.png")
background_label = Label(app, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Bouton Choose File
add_btn = Button(app, text='Choose File', width=12, command=chooseFile)
add_btn.place(x=200, y=200)

# Bouton Detect
add_btn = Button(app, text='Detect', width=12, command=execAI)
add_btn.place(x=100, y=200)

# Label
part_label = Label(app, text='Do you have Parkinson ?', bg='#facd54', font=('bold', 14), pady=20)
part_label.place(x=185, y=105)

if os.path.exists("recordingAudio.wav"):
    os.remove("recordingAudio.wav")

# App title
app.title('AI Parkinson Detector')
app.geometry('600x400')
App(app)
app.mainloop()

