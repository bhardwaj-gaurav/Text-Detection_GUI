import cv2
import pytesseract
from tkinter.ttk import *
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image


root = Tk()
root.geometry('665x500+500+150')
Frm = Frame(root, width=350, height=400, highlightbackground="black", highlightthickness=4)
Frm.pack()

def quit():
    root.withdraw()

def Filed():
    filename = askopenfilename(initialdir="/", title="select",
                               filetypes=[('image', '*.jpg'), ('image', '*.jpeg'), ('image', '*.png'),
                                          ('image', '*.svg')])
    file = str(filename)
    lst.insert(END, file)

def show(e):
    n = lst.curselection()
    fname = lst.get(n)
    print(fname)
    images = Image.open(fname)
    images = images.resize((650, 400), Image.ANTIALIAS)
    imgg = ImageTk.PhotoImage(images)
    canvas.create_image(0, 0, image=imgg, anchor=NW)
    canvas.image = imgg

lst = Listbox(Frm, height=5)
lst.pack(side=TOP, fill=X, expand=-0.5)
lst.bind("<<ListboxSelect>>", show)

canvas = Canvas(Frm, width=650, height=400, bg='blue')
canvas.pack(side='left')
images = Image.open('Image\\back.png')
images = images.resize((650, 400), Image.ANTIALIAS)
imgg = ImageTk.PhotoImage(images)
canvas.create_image(0, 0, image=imgg, anchor=NW)

btn = Button(Frm, text="Choose Image", command=Filed, width=14, height=2)
btn.place(x=10, y=430)

btn = Button(Frm, text="Quit", command=quit, width=14, height=2)
btn.place(x=270, y=430)

def detect():

    n = lst.curselection()
    w = lst.get(n)
    pytesseract.pytesseract.tesseract_cmd = 'Tesseract\\tesseract.exe'

    img = cv2.imread(w)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))

    dilation = cv2.dilate(thresh1, rect_kernel, iterations=7)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    im2 = img.copy()

    file = open("recognized.txt", "w+")
    file.write("")
    file.close()

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cropped = im2[y:y + h, x:x + w]

    file = open("recognized.txt", "a")
    text = pytesseract.image_to_string(cropped)

    file.write(text)
    file.write("\n")
    file.close()
    ##############################################################

    ##############################################################
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    hImg, wImg, _ = img.shape
    boxes = pytesseract.image_to_boxes(img)
    for b in boxes.splitlines():
        print(b)
        b = b.split(' ')
        print(b)
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (50, 50, 255), 2)
        cv2.putText(img, b[0], (x, hImg - y + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)

    cv2.imshow('img', img)
    cv2.waitKey(0)

btn1 = Button(root, text="Detect Text", command=detect, width=14, height=2)
btn1.place(x=530, y=435)
root.mainloop()
