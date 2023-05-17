import cv2, os, mysql.connector, time, random, tkinter as tk, numpy as np
import xml.etree.ElementTree as ET
from random import randint, randrange
from tkinter.ttk import *
from tkinter import *
import customtkinter
from PIL import Image, ImageTk
from ctypes import windll

connect = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="",
    database="face-recog")

windll.shcore.SetProcessDpiAwareness(1)
pp = 0
gnemon = 0
root = Tk()

cam = cv2.VideoCapture(0)
root.attributes("-fullscreen", True)
root.title("Face-Recognition")
root.wm_attributes('-transparentcolor', '#ab23ff')

bg = Image.open("img/bg.png")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
bg = bg.resize((width, height), Image.ANTIALIAS)
bg = ImageTk.PhotoImage(bg)
bg_label = Label(root, image=bg)
bg_label.place(x=0, y=0)

# btn1 = Button(root, text='Quit !', command=root.destroy)
# btn1.grid(row=0, column=3, padx=100)

d_data=1
faceID = 0
prevT = 0
bbl = []
d_bool_IO23 = False
complete_bool = False
hasil = 0
faceNM = ''
bye = False
timer_ = False
start_ = False
scan = False
name_afScan = []
scan_ = True
nm_temp = ['']
score_nm = [0] * 120 # IMP
hasil_ = 0
_start_ = False
xml_bool = False
welcomeL = False
welcomeR = False
where = ''

nxt = Button(root)
klr_img = Image.open("img/back 100x100.png")
img_resize = klr_img.resize((75, 75))
klr_btn = ImageTk.PhotoImage(img_resize)
klr = Label(root)
parent1 = Frame(root)
dataR = Label(root)
dataR.place(x=0,y=0)
lbl = Label(root)
l = Label(root)
inpt = Entry(root)
register_btn = Button(root)
parent = Frame(root)

home = Image.open("img/home.png")
home_resize = home.resize((50, 50))
home_btn = ImageTk.PhotoImage(home_resize)
home_last = Label(root)


def register(event):
    global inpt, l, inpt, register_btn, dataR,parent1, klr
    klr.destroy()
    # cam.release()
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 100)
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    back_icon("register")
    # frame.destroy()
    l3.destroy()
    btn1.destroy()
    l2.destroy()
    cam2lbl()
    l.config(text = "\" Isi Nama mu Terlebih Dahulu ! \"")

    def stateENM(event): 
        inpt.config(state=NORMAL)
        inpt.delete(0, END)

    inpt = Entry(root,textvariable='', width=20, font=('Arial', 12, 'normal'))
    inpt.place(relx=0.7, rely=0.5)
    inpt.insert(0, "Your Name")
    inpt.config(state=DISABLED)
    inpt.bind("<Button-1>", stateENM)

    register_btn = Button(root, font=('Poppins SemiBold',11), text='REGISTER', bg='dodgerblue', fg='white', width=13, height=1 ,bd=10,
              borderwidth=3, highlightcolor='#59C3FF', highlightthickness=3, highlightbackground="#59C3FF" ,command=dtbs_IO_insert)
    register_btn.place(relx=0.76, rely=0.60, anchor=CENTER)

    img2 = ImageTk.PhotoImage(Image.open("img/done.png"))
    # print(img2)
    lbl.place(relx=0.33, rely=0.4)
    root.update()
    return minW, minH



def dtbs_IO_insert() :
    global inpt, l, d_bool_IO23, faceNM, faceID, register_btn, start_
    register_btn["state"] = "disable"
    register_btn.config(bg="grey")
    d_bool_IO23 = True
    start_ = True

    faceNM = inpt.get()
    print("1 Clicked", faceNM)
    for row in rows:
        faceID = row[0]+1
        if (faceNM != row[1]) :
            bbl.append(0)
            # break
        else :
            bbl.append(1)
            # break
    x=0
    for i in bbl:
        if(i == 1) :
            print("Nama sudah ada dalam Data !!!")
            faceID = rows[x][0]
            break;
            
        x+=1
        # if len(bbl) == x+1 and i == 0:

    if 1 not in bbl :
        csr.execute("INSERT INTO identity_test(id, nama) VALUES({}, '{}')".format(faceID, faceNM))
        connect.commit()
        l.config(text="\" Nama Sudah Dimasukkan Ke dalam Data \"")
        faceID = rows[x-1][0] + 1



def welcome_IO():
    global faceNM, bye, welcomeL, welcomeR, home_last, parent, klr

    lbl.destroy()
    inpt.destroy()
    register_btn.destroy()
    l.destroy()
    klr.destroy

    nxt.destroy()

    home_last = Label(image=home_btn, bg="white", borderwidth=0, highlightthickness=0)
    home_last.bind("<Button>", utama)
    home_last.place(relx= 0.5, rely= 0.9, anchor=CENTER)
    
    parent = Frame(root)
    l4 = Label(parent, text = "Welcome, {}".format(faceNM), font=('Poppins SemiBold', 30), fg="Black", bg="white").pack(fill='x')
    parent.pack(expand=1)

    bye = True

    if welcomeL == True:
        back_icon("welcomeL")
    elif welcomeR == True:
        back_icon("welcomeR")


def login() :
    global timer_, scan, nxt, klr_img, klr
    klr.destroy()
    back_icon("login")

    timer_ = True
    l3.destroy()
    btn1.destroy()
    l2.destroy()
    cam2lbl()
    nxt = Button(root, font=('Poppins SemiBold',12), text='Next', bg='dodgerblue', fg='white', width=15,bd=10,
              borderwidth=3, highlightcolor='#59C3FF', highlightthickness=3, highlightbackground="#59C3FF" ,command=welcome_IO)
    nxt.place(relx=0.7, rely=0.50)

    nxt["state"] = "disable"
    nxt.config(bg="grey",)
    lbl.place(relx=0.33, rely=0.4)
    root.update()


def data_io(path):
    imageFile = [os.path.join(path,i) for i in os.listdir(path)]
    faceSamples = []
    faceIDs = []
    for imagef in imageFile:
        PILimage = Image.open(imagef).convert('L')
        imgNum = np.array(PILimage,'uint8')
        faceID = int(os.path.split(imagef)[-1].split(".")[0].replace('face',''))
        faces = faceDetector.detectMultiScale(imgNum)
        for(top,right,down,left) in faces:
            faceSamples.append(imgNum[right:right+left, top:top+down])
            faceIDs.append(faceID)
    return faceSamples, faceIDs


def xml_inpt() :
    global nxt, bye, complete_bool, dataR, timer_, start_, xml_bool,parent1
    bye = True
    l.destroy()
    lbl.destroy()
    register_btn.destroy()
    inpt.destroy()

    parent1 = Frame(root)
    dataR = Label(parent1, text = "Sedang Menyiapkan Data...", font=('Poppins SemiBold', 25), fg="Black", bg="white").pack(fill='x')
    parent1.pack(expand=1)
    root.update()
    faces, IDs = data_io('faceData')
    recognizer.train(faces, np.array(IDs))
    recognizer.write('xml/training.xml')
    complete_bool = False
    timer_ = True
    start_ = False
    xml_bool = True

def utama(event):
    global lbl, btn1, l2, frame_, l3, bye, inpt, l, register_btn, nxt, recognizer, csr, rows, back, home_last, parent
    global scan, scan_, timer, timer_, hasil, start_

    # RESET ALL VARIABLE 


    scan = False
    scan_ = False
    timer = False
    timer_ = False
    start_ = False
    hasil = 0

    # DESTROY WIDGES 
    parent1.destroy()
    parent.destroy()
    lbl.destroy()
    nxt.destroy()
    l.destroy()
    inpt.destroy()
    register_btn.destroy()
    klr.destroy()
    home_last.destroy()


    back = Label(text = "", font=('Poppins Medium',13), fg="#969696", bg="white")
    back.place(relx=0.5, rely=0.60, anchor=CENTER)
    csr = connect.cursor()
    query = "SELECT * FROM identity_test"
    csr.execute(query)
    rows = csr.fetchall()
    bye = False
    lbl = Label(root, width=0)
    lbl.place(relx=0.5, rely=0.40, anchor=CENTER)
    btn1 = customtkinter.CTkButton(master = root, text_font=('Poppins SemiBold',12), text='Login', bg_color='white', 
                fg_color='dodgerblue', text_color='white', width=405,height=55, corner_radius=30,command=login)
    btn1.place(relx=0.5, rely=0.80, anchor=CENTER)
    l2 = Label(root, text = "Belum Memiliki akun ?", font=('Poppins Medium',12), fg="black", bg="white")
    l2.place(relx=0.424, rely=0.85)
    frame_ = Frame(root, bg='white')
    frame_.place(relwidth=0.06, relheight=0.09, relx=0.5425, rely=0.85)
    l3 = Label(frame_, text = "Daftar !", font=('Poppins Medium',12), fg="dodgerblue", bg="white")
    l3.place(relx=0, rely=0)
    l3.bind("<Button-1>", register)
    inpt = Entry(root,textvariable='', width=0)
    l = Label(root, text = "", font=('Poppins Medium',13), fg="Black", bg="white")
    l.place(relx=0.20, rely=0.73)
    register_btn = Button(root)
    nxt = Button(root)

def back_back(event):
    global where
    print("Weawea")
    if where == "register" or where == "login" :
        print("erereh")
        return utama('')
    elif where == "welcomeL":
        return login()
    elif where == "welcomeR":
        return register()

def back_icon(path):
    global klr, where
    where = path
    klr = Label(image=klr_btn, bg="#87D0C9", borderwidth=0, highlightthickness=0)
    klr.bind("<Button>", back_back)
    klr.place(x=50, y=25)
    print(where, path)

# back_icon("login")

address = "http://192.168.1.4:8080/video"

faceDetector = cv2.CascadeClassifier('xml/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

utama('')

if os.path.exists('xml/training.xml') :
    recognizer.read('xml/training.xml')

id = ''
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 700)
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)
start_IO23_bool = False
while True:
    # print(f_encoding)
    ret, frame = cam.read()
    frame = cv2.flip(frame, 1)
    abuAbu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    facess = faceDetector.detectMultiScale(
            abuAbu, 1.2, 15, minSize=(round(minW ), round(minH)),)

    currentT = time.time()
    if timer_ == True and xml_bool == True:
            if(start_ == False) :
                start_ = True
                countdown = int(currentT)+4
            hasil = countdown - int(currentT)
            back.config(text="Kembali ke Halaman Login dalam ({})".format(hasil))
                # print(int(hasil), countdown, int(current))

            if hasil==0:
                back.destroy()
                utama('')
                timer_ = False
                start_ = False
                xml_bool = False
                
    root.update()
    if bye != True:
        if timer_ == True:
            if(start_ == False) :
                start_ = True
                countdown = int(currentT)+4
            hasil = countdown - int(currentT)
                # print(int(hasil), countdown, int(current))
            l.config(text = "\" Scan Akan Dimulai dalam {} Detik ! \"".format(hasil))
    
        if int(hasil) == 0 and timer_ == True or scan == True and scan_ == True:
            if start_ == True :
                scan = True
                start_ = False
            if (_start_ == False):
                _start_ = True
                countdown = int(currentT)+4
            if hasil_ == 0 :
                countdown = int(currentT)+3
            hasil_ = countdown - int(currentT)
            if (hasil_ == 3):
                l.config(text = "Scanning...")
            elif (hasil_  == 2):
                l.config(text = "Scanning..")
            elif (hasil_ == 1):
                l.config(text = "Scanning.")
            timer_ = False
            print("FLSFLS")

        if complete_bool == True :
            xml_inpt()
            # dataR.destroy()
            # l.config(text="\" Record Selesai \"")
            # if complete_bool == True and int(currentT) % 3 == 0 and int(currentT) != int(prevT):
            #     complete_bool = False
            #     welcome_IO()

        scanActive = False

        for (x, y, w, h) in facess:
            scanActive = True

            if scanActive == True :
                scan_ = True

            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            if os.path.exists('xml/training.xml') :
                id, confidence = recognizer.predict(abuAbu[y:y+h, x:x+w])
            nameID = 'Unknown'


            # FOR REGISTER, DELAY RECORD FACE AND TEXT
            # FOR REGISTER, DELAY RECORD FACE AND TEXT
            # FOR REGISTER, DELAY RECORD FACE AND TEXT

            if d_data % 5 == 0 and d_bool_IO23 == True and d_data != 0:
                    if hasil == 0:
                        countdown = int(currentT) + 2
                    hasil = countdown - int(currentT)
            if hasil == 0 and d_bool_IO23 == True or d_data == 0 and d_bool_IO23 == True:
                    start_ = False
                    fileName = 'face'+str(faceID)+'.'+str(d_data)+ str(random.randrange(100, 999)) + '.jpg'
                    d_data += 1
                    cv2.imwrite('faceData/' + fileName,frame)
                    l.config(text = "\" Sedang Merekam Wajah ({}/20) \"".format(d_data))

            # UNTIL HERE

            prevT = currentT

            if os.path.exists('xml/training.xml'):
                if confidence <= 50:
                    for row in rows:
                        if (id == row[0]):
                            nameID = row[1]
                            if (scan == True):
                                if len(name_afScan) >= 120:
                                    # print(name_afScan)
                                    l.config(text="\" Scan Complete \"")
                                    timer_ = False
                                    scan = False
                                    for i in name_afScan:
                                        bol21 = 0
                                        for m in nm_temp:
                                            if i == m:
                                                num = nm_temp.index(m)
                                                score_nm[num] += 1
                                                bol21 = 1
                                        if bol21 == 0 :    
                                            nm_temp.append(i)
                                    faceNM = nm_temp[score_nm.index(max(score_nm))]
                                    nxt["state"] = "normal"
                                    nxt.config(bg="dodgerblue")
                            break
                    confidencetxt = " {0}%".format(round(100-confidence))
                else:
                    confidencetxt = " {0}%".format(round(100-confidence))
                if scan == True:
                    name_afScan.append(nameID)

            font = cv2.FONT_HERSHEY_DUPLEX
            
            cv2.putText(frame, str(nameID), (x+5, y-5),
                        font, 1, (200, 255, 100), 2)
        framecv2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if (scanActive == False and scan == True) :
            scan_ = False
            l.config(text="\" Posisikan Wajahmu di depan Kamera \"")
        def cam2lbl():
            img = Image.fromarray(framecv2)
            imgTk = ImageTk.PhotoImage(image=img)
            lbl.imgTk = imgTk
            lbl.configure(image=imgTk)
        if(bye == False):
            cam2lbl()   
        key = cv2.waitKey(1) & 0xFF
        
    if d_data == 20 :
        d_bool_IO23 = False
        complete_bool = True
        d_data = 0
    def close_win(e):
        root.destroy()
    root.bind('<Escape>', lambda e: close_win(e))