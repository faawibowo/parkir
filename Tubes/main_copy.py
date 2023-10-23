import time
import datetime
import math
from tkinter import *
import pyqrcode
import cv2
import tkinter as tk
from functools import partial


def masuk(database:list, user:int):
    waktu_masuk = time.time()
    database.append(waktu_masuk)
    user += 1
    print(f"Nomor user anda adalah {user}")
    show_QR(user)
    
    return user


def keluar(database:list, PRICE:int):
    while True:
        # user = int(input("Masukkan nomor user: "))
        user = None
        cap = cv2.VideoCapture(0) 
        # initialize the cv2 QRCode detector 
        detector = cv2.QRCodeDetector()
        
        while True: 
            _, img = cap.read()
            if img is None:
                continue

            # detect and decode 
            data, bbox, _ = detector.detectAndDecode(img)
            # check if there is a QRCode in the image 
            if data: 
                user=int(data)
                break
            
            cv2.imshow("QRCODEscanner", img)
            if cv2.waitKey(1) == ord("q"):
                break

        cap.release() 
        cv2.destroyAllWindows()

        if database[user - 1] != None:
            waktu_masuk = database[user - 1]
            waktu_keluar = time.time()
            total_price = 0
            if (waktu_keluar - waktu_masuk) > 3600:
                total_price = PRICE * math.ceil((waktu_keluar - waktu_masuk)/3600)
            else:
                total_price = 2000
            print(f"Lama anda adalah {datetime.timedelta(seconds=(waktu_keluar - waktu_masuk))}, total harga adalah {total_price}")
            database[user - 1] = None
            break
        else:
            print("User telah keluar")
            break

def show_QR(user:int):
    ws = Tk()
    ws.title("QR")
    ws.config(bg='#FFFFFF')

    img_lbl = Label(
        ws,
        bg='#FFFFFF')
    img_lbl.pack()
    output = Label(
        ws,
        text="",
        bg='#FFFFFF'
        )
    output.pack()

    qr = pyqrcode.create(user)
    img = BitmapImage(data = qr.xbm(scale=8))

    try:
        img_lbl.config(image = img)
        output.config(text="QR code of " + user)
    except:
        pass
    
    ws.mainloop()

PRICE = 2000
database = []
user = 0

root = tk.Tk()
root.title("Masuk Function Example")


# Create a button that calls the masuk_function when clicked
button = tk.Button(root, text="Masuk", command=lambda: masuk(database,  user))
button.pack()


    
root.mainloop()
