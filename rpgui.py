from cProfile import label
from email.mime import image
from glob import glob1
from tkinter import *
from PIL import ImageTk, Image




root=Tk()
canvas=Canvas(root,width=1275,height=999)
bg=Image.open("C:\\Users\\prath\\GUI_SIH\\Gesture_Detection\\Gui_images\\bg2.jpg")
sid = Image.open("C:\\Users\\prath\\GUI_SIH\\Gesture_Detection\\Gui_images\\sid.jpg")
#bg.paste(sid,(20,40), sid)
Image=ImageTk.PhotoImage(bg)

ges1=Button(root, text="Save",font=('Helvatica 20 bold italic') ,fg="black",bg="white",height=2,width=15).place(x=1100,y=75)
ges2=Button(root, text="Close Window",font=('Helvatica 20 bold italic') ,fg="white",bg='black',height=2,width=15).place(x=1100,y=225)
ges3=Button(root, text="Print",font=('Helvatica 20 bold italic') ,fg="white",bg="black",height=2,width=15).place(x=1100,y=375)
ges4=Button(root, text="Lock Workstation",font=('Helvatica 20 bold italic') ,fg="white",bg='black',height=2,width=15).place(x=1100,y=525)
ges5=Button(root, text="Restart",font=('Helvatica 20 bold italic') ,fg="white",bg="black",height=2,width=15).place(x=1100,y=675)



#label(root,text="GesSure",font=("Arial",30,"bold"),bg="black",fg="white").pack()
canvas.create_image(0,0,anchor=NW,image=Image)
canvas.pack()
root.configure(bg="black")
root.mainloop()