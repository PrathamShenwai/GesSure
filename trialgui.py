from cProfile import label
from email.mime import image
from tkinter import *
from PIL import ImageTk, Image




root=Tk()
canvas=Canvas(root,width=1599,height=999)
Image=ImageTk.PhotoImage(Image.open("C:\\Users\\prath\\GUI_SIH\\Gesture_Detection\\Gui_images\\bg1.jpg"))
#label(root,text="GesSure",font=("Arial",30,"bold"),bg="black",fg="white").pack()
canvas.create_image(0,0,anchor=NW,image=Image)
canvas.pack()

def login():
    root.destroy()
    loginclick = Tk()
    #c2=Canvas(loginclick,width=1599,height=999)
    loginclick.title("Verification in process")
    bg2=Image.OPEN("C:\\Users\\prath\\GUI_SIH\\Gesture_Detection\\Gui_images\\bg2.jpg")
    Img=ImageTk.PhotoImage(bg2)
    #c2.create_image(0,0,anchor=NW,image=Img)
    loginclick.configure(background="black")
    loginclick.geometry('1599x999')
    

create_dataset=Button(root, text="Login",command=login,font=('Helvatica 20 bold italic') ,fg="white",bg="black",height=3,width=20).place(x=650,y=450)
train_dataset=Button(root, text="Register",font=('Helvatica 20 bold italic') ,fg="white",bg='black',height=3,width=20).place(x=650,y=650)

root.configure(bg="red")
root.mainloop()

