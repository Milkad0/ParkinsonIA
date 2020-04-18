from tkinter import *
from tkinter import filedialog
from lib.RecognitionLib import *

global filePath
global clf

path = "lib/trainedModel.sav"
clf = loadModel(path)
filePath = "unknow"


def chooseFile():
    global filePath
    filePath = filedialog.askopenfilename(initialdir="/C", title="Select a file", filetypes=[("wav file", "*.wav")])
    print("path :", filePath)


def execAI():
    global part_label1
    global part_label2
    global part_label3

    errmsg = "Path not valid"
    if (filePath != "unknow") and (filePath != ""):
        if predict(clf, filePath):
            # Test label3
            try:
                part_label3
            except NameError:
                part_label3 = None

            if part_label3 is not None:
                part_label3.destroy()

            # Test label2
            try:
                part_label2
            except NameError:
                part_label2 = None

            if part_label2 is not None:
                part_label2.destroy()

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

        # Display answer
        part_label3 = Label(app, text=errmsg, font=('bold', 14), bg='#facd54', pady=20)
        part_label3.place(x=400, y=105)

        print(errmsg)
        return errmsg


# Create Window
app = Tk()
app.resizable(False, False)

# background
filename = PhotoImage(file="img/bn3-bg.png")
background_label = Label(app, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Bouton Choose File
add_btn = Button(app, text='Choose File', width=12, command=chooseFile)
add_btn.place(x=300, y=200)

# Bouton Detect
add_btn = Button(app, text='Detect', width=12, command=execAI)
add_btn.place(x=200, y=200)

# Label
part_label = Label(app, text='Do you have Parkinson ?', bg='#facd54', font=('bold', 14), pady=20)
part_label.place(x=185, y=105)


# App title
app.title('AI Parkinson Detector')
app.geometry('600x400')

app.mainloop()

pause = input("pause...")