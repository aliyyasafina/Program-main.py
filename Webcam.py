import sys
sys.path.append('/usr/local/lib/python3.9/site-packages')
import cv2
import time
from pyzbar.pyzbar import decode

from ubidots_get_post import *
from scan_rfid import *

# set up camera object called Cap which we will use to find OpenCV
cap = cv2.VideoCapture(0)

total_belanja = 0

daftar_barang = {
    "Keripik Ubi Ungu": 2000,
    "Roti O" : 2000,
    "Kebab" : 3000,
    "Bolu Pisang" : 2000,
    "Puding coklat" : 2000,
    "Kue Pisang": 2000
}

#This creates an Infinite loop to keep your camera searching for data at all times
def scan_product(payProduct):
    # cap = cv2.VideoCapture(0)
    global total_belanja
    
    # Below is the method to get a image of the QR code
    ret, frame = cap.read()
    # resize_image = cv2.resize(frame, (176, 144))
    
    # Read the QR code by detetecting the bounding box coords and decoding the hidden QR data 
    if ret:
        for d in decode(frame):
            data = d.data.decode()
            frame = cv2.rectangle(frame, (d.rect.left, d.rect.top),
                                  (d.rect.left + d.rect.width, d.rect.top + d.rect.height), (0, 255, 0), 3)
            frame = cv2.putText(frame, data, (d.rect.left, d.rect.top + d.rect.height),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
            
            if data:
                print("data found: ", data)
                print(daftar_barang[data])        
                total_belanja += daftar_barang[data]
                print("total belanja: ", total_belanja)
                #send_text("dashboard-text", "Scan berhasil, produk {} Rp{}, \nTotal belanja anda Rp{}".format(data, daftar_barang[data], total_belanja))
            
        # Below will display the live camera
        cv2.imshow("QR Detector",frame)
        cv2.moveWindow("QR Detector", 200, 200)
    
    # 4. Jika sudah selesai belanja, klik tombol Bayar di Ubidots lalu tap kartu
    if (payProduct):
        print("Pay Product")
        send_text("dashboard-text", "Silahkan lakukan pembayaran! Total belanja anda, {}".format(total_belanja))
        cap.release()
        cv2.destroyAllWindows()
        tap_update_saldo(total_belanja) # 5. Tap kartu untuk bayar
        return False

    
    #At any point if you want to stop the Code all you need to do is press 'q' on your keyboard
    if(cv2.waitKey(1) == ord("q")):
        cap.release()
        cv2.destroyAllWindows()
