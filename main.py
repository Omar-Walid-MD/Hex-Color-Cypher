from customtkinter import *
from PIL import Image, ImageDraw, ImageColor, ImageGrab, ImageTk
from io import BytesIO
import win32clipboard

def printText():
    global resultCanvasImage
    hex = plaintext.get().encode("utf-8").hex()
    # print(hex)
    hex += "0"*(6-len(hex)%6 if len(hex)%6 else 0)

    hexArray = ["#"+hex[i:i+6] for i in range(0,len(hex),6)]
    img = Image.new("RGB",(len(hexArray)*blockSize,blockSize))
    d = ImageDraw.Draw(img)
    for i,hexColor in enumerate(hexArray):

        color = ImageColor.getcolor(hexColor, "RGB")
        d.rectangle((i*blockSize,0,i*blockSize+blockSize,blockSize),color)
    
    sendToClipboard(img)

    w = min(img.width,600)
    h = min(img.height,400)
    resultCanvasImage = ImageTk.PhotoImage(img.resize((w,h)))
    resultCanvas.create_image(0, 0,anchor="nw",image=resultCanvasImage)
    print("done")

def sendToClipboard(image):
    output = BytesIO()
    image.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard() 
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

def decodeImage():
    imgInClip = ImageGrab.grabclipboard()
    result = ""
    for x in range(int(imgInClip.width/blockSize)):
        hex = '%02x%02x%02x' % imgInClip.getpixel((x*blockSize,0))
        result += bytearray.fromhex(hex).decode()

    resultText.delete('1.0', END)
    resultText.insert("0.0",result)
    
    

blockSize = 50

root = CTk()
root.title("Hex Color Cypher")
root.geometry("500x335")
root.resizable(False,False)

tabview = CTkTabview(root)
tabview.pack(pady=0)

encodeTab = tabview.add("Encode")
decodeTab = tabview.add("Decode")


encodeInputFrame = CTkFrame(encodeTab)
encodeInputFrame.pack(anchor="n",padx=20,fill="x")

decodeInputFrame = CTkFrame(decodeTab)
decodeInputFrame.pack(anchor="n",padx=20,fill="x")


CTkLabel(encodeInputFrame,text="Enter Text:").pack(anchor="w",side="top")

plaintext = StringVar()
textInput = CTkEntry(encodeInputFrame,textvariable=plaintext)
textInput.pack(side="top",fill="x")

submitTextButton = CTkButton(encodeInputFrame,text="Enter Text",command=printText,width=50)
submitTextButton.pack(expand=True,pady=5)

resultCanvas = CTkCanvas(encodeTab,width=600,height=400,bg="white",highlightthickness=1,highlightbackground="black")
resultCanvas.pack(pady=5)
resultCanvasImage = None

resultText = CTkTextbox(decodeTab,height=200,border_width=2)
resultText.pack(pady=5,fill="x")

submitImageButton = CTkButton(decodeInputFrame,text="Paste Image from Clipboard",command=decodeImage)
submitImageButton.pack(expand=True,pady=5)


root.mainloop()
