import cv2
import tkinter as tk
from tkinter.ttk import *
from tkinter import * 
from PIL import Image, ImageTk

root = Tk()
style = Style()

root.title("Face Recognition")
root.attributes('-fullscreen', True)
bg = Image.open("Blue Green Watercolor Linktree Background.png")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
bg = bg.resize((width, height), Image.ANTIALIAS)
bg = ImageTk.PhotoImage(bg)
bg_label = Label(root, image=bg)
bg_label.place(x=0, y=0)

cam = cv2.VideoCapture(0)
lbl = Label(root, width=0)
lbl.place(relx=0.5, rely=0.40, anchor=CENTER)

def text_login():
    txt_lgn = Label(root, text="Login", 
                    fg="#57A1F8", 
                    bg="#FFFFFF",
                    font=("Microsoft Sans Serif", 34, "bold"))
    txt_lgn.place(relx=0.5, rely=0.1, anchor=CENTER)

    lgn = Button(root, text="Login", 
                 font=("Times New Roman", 16), 
                 bg="#57A1F8", fg="white",
                 height=2, width= 40,
                 borderwidth=1)
    lgn.place(relx=0.5, rely=0.8, anchor=CENTER)
text_login()

def button_keluar():
     root.destroy()

klr = Button(root, text="Keluar", font=("Arial", 14), command=button_keluar)
klr.pack()
klr.place(x = 100, y = 100)

while True:
    # print(f_encoding)
    root.update()
    ret, frame = cam.read()
    frame = cv2.flip(frame, 1)
    framecv2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def cam2lbl():
        img = Image.fromarray(framecv2)
        imgTk = ImageTk.PhotoImage(image=img)
        lbl.imgTk = imgTk
        lbl.configure(image=imgTk)
    cam2lbl()
            
    key = cv2.waitKey(0) & 0xFF
    if key == 27:  # to close video capture
        print("Close")
        root.destroy()
        break

root.mainloop()