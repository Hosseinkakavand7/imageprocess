from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pathlib
from tkinter import Entry, Button, Frame, Tk, filedialog, INSERT, Radiobutton, IntVar
from subprocess import check_output


def histogram(img):
    pixel = [0] * 256
    for i in range(0, len(img)):
        for j in range(0, len(img[1])):
            pixel[img[i][j]] += 1
    return pixel
def pixel_change(mode, scale, img):
    image=img
    if mode == 1:                                           #plus
        for i in range(0, len(image)):
            for j in range(0, len(image[1])):
                if image[i][j] + scale > 255:
                    image[i][j] = 255
                elif image[i][j] + scale < 0:
                    image[i][j] = 0
                else:
                    image[i][j] += scale

    elif mode == 2:                                         #multiply
        for i in range(0, len(image)):
            for j in range(0, len(image[i])):
                if image[i][j] * scale > 255:
                    image[i][j] = 255
                elif image[i][j] * scale < 0:
                    image[i][j] = 0
                else:
                    image[i][j] *= scale

    elif mode == 3:                                         #power
        for i in range(0, len(image)):
            for j in range(0, len(image[i])):
                q=image[i][j]/255.0
                q=q**scale
                q=q*255
                if (q) > 255:
                    image[i][j] = 255
                elif q < 0:
                    image[i][j] = 0
                else:
                    image[i][j] = q

    return image
def browsefunc(add_entry):
    fileadd = filedialog.askopenfilename(title="Select file", filetypes=(
    ("Image Files ", "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.tiff"), ("all files", "*.*")))
    add_entry.delete(0,len(add_entry.get()))
    add_entry.insert(INSERT, fileadd)
def minus(image1,image2):
    image=image1
    for i in range(0,len(image)):
        for j in range(0,len(image[1])):
            if int(image1[i][j])-int(image2[i][j])>=0:
                image[i][j]=image1[i][j]-image2[i][j]
            else:
                image[i][j]=image2[i][j]-image1[i][j]
    return image
def work(img,type,scale,x,y,z,plot_title,x_axis,rec):
    image=img
    if type!=0:
        image=pixel_change(type,scale,image)
    sum=0
    if rec:
        for q in range(0,len(image)):
            for t in range(0,len(image[1])):
                sum+=image[q][t]
    photo=Image.fromarray(image)
    plt.subplot(x,y,z+y)
    plt.imshow(photo)
    plot = histogram(image)
    plt.subplot(x,y,z,title=plot_title,xlabel=str(sum))
    plt.plot(x_axis, plot, "b.")
    return image
def start(add, plus_ent, multi_ent, pow_ent):
    x_axis = []
    for i in range(0,256):
        x_axis.append(i)
    address = add.get()
    var=[]
    var.append(plus_ent.get())
    var.append(multi_ent.get())
    var.append(pow_ent.get())
    for i in range(0,len(var)):
        if var[i]!="":
            var[i]=eval(var[i])
        else:
            if i == 0:
                var[i]=0
            else:
                var[i]=1
    opt=option.get()
    if opt!=5:
        if opt!=4:
            n=1
        else:
            n=3
        for i in range(1,n+1):
            images=[]
            plt.figure(i)
            if n>1 and i==1:
                opt=1
            elif n>1 and i!=1:
                opt+=1
            print (var[opt-1])
            image_1= np.array(Image.open(pathlib.WindowsPath(address)).convert("L"))
            images.append(work (image_1,0,0,2,4,1,"A=Original",x_axis,False))
            image_1= np.array(Image.open(pathlib.WindowsPath(address)).convert("L"))
            images.append(work (image_1,opt,var[opt-1],2,4,2,"B=G(Original,V)",x_axis,False))
            image_1= np.array(Image.open(pathlib.WindowsPath(address)).convert("L"))
            keep=minus(image_1,images[1])
            images.append(work (keep,0,var[opt-1],2,4,4,"D=A-B",x_axis,True))
            if opt==1:
                images.append(work (images[1],opt,-var[opt-1],2,4,3,"C=G(B,-V)",x_axis,False))
            else:
                images.append(work (images[1],opt,1/var[opt-1],2,4,3,"C=G(B,-V)",x_axis,False))
            print(i,":Done")
        if n>1:
            plt.figure(1,title="Plus")
            plt.figure(2,title="Multiply")
            plt.figure(3,title="Power")
            plt.show()
        else:
            if opt==1:
                q="Plus"
            elif opt==2:
                q="Mutiply"
            elif opt==3:
                q="power"
            plt.figure(1,title=q)
            plt.show()
    else:
        x_axis = []
        for i in range(0,108):
            x_axis.append(i)
        i=len(address)-1
        name=""
        while address[i]!="/":
            name=address[i]+name
            i-=1
        featfind=r"C:\Users\hossein\Desktop\Histogram\featfind\featfind.exe"
        values=check_output([featfind,address,name],universal_newlines=True)
        values=values.split(",\n")
        values.pop()
        for i in range(0,len(values)):
            values[i]=float(values[i])
        plt.subplot(1,2,1)
        plt.plot(x_axis,values,"b.")
        image= np.array(Image.open(pathlib.WindowsPath(address)).convert("RGB"))
        plt.subplot(1,2,2)
        photo=Image.fromarray(image)
        plt.imshow(photo)
        plt.show()


root = Tk()
root.geometry("500x200")
address_frame = Frame(root, height=300, width=500, bg="#f0f0f0")
option = IntVar()
R1 = Radiobutton(address_frame, text="+", variable=option, value=1)
R1.select()
R2 = Radiobutton(address_frame, text="*", variable=option, value=2)
R3 = Radiobutton(address_frame, text="^", variable=option, value=3)
R4 = Radiobutton(address_frame, text="all", variable=option, value=4)
R5 = Radiobutton(address_frame, text="Feat", variable=option, value=5)

Address = Entry(address_frame, width=70)
plus_entry= Entry(address_frame)
multi_entry= Entry(address_frame)
power_entry= Entry(address_frame)

browse_button = Button(address_frame, text="Browse", command=lambda: browsefunc(Address))
submit_button = Button(address_frame, text="Submit", command=lambda: start(Address, plus_entry, multi_entry, power_entry))

address_frame.place(x=0, y=0)

Address.place(x=10, y=20)

browse_button.place(x=445, y=17)
R1.place(x=88, y=50)
plus_entry.place(x=188,y=50)
R2.place(x=88, y=75)
multi_entry.place(x=188,y=75)
R3.place(x=88, y=100)
power_entry.place(x=188,y=100)
R4.place(x=88, y=122)
R5.place(x=88, y=144)

submit_button.place(x=227, y=170)

root.mainloop()
