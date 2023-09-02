import sys
sys.path.append('/usr/local/lib/python3.9/site-packages')
import cv2
import time

from ubidots_get_post import *
from scan_rfid import *

# set up camera object called Cap which we will use to find OpenCV
cap = cv2.VideoCapture(0)

# QR code detection Method
detector = cv2.QRCodeDetector()

total_belanja = 0

daftar_barang = {
    "Keripik Ubi Ungu": 2000,
    "Roti O" : 2000,
    "Kebab" : 3000,
    "Bolu Pisang" : 2000,
    "Puding coklat" : 2000,
}

#This creates an Infinite loop to keep your camera searching for data at all times
def scan_product():
    # Below is the method to get a image of the QR code
    _, img = cap.read()
    resize_image = cv2.resize(img, (176, 144))
    
    # Read the QR code by detetecting the bounding box coords and decoding the hidden QR data 
    data, bbox, _ = detector.detectAndDecode(resize_image)
    
    # This is how we get that Blue Box around our Data. This will draw one, and then Write the Data along with the top (Alter the numbers here to change the colour and thickness of the text)
    global total_belanja
    if(bbox is not None):
        for i in range(len(bbox)):
            if data:
                print("data found: ", data)
                print(daftar_barang[data])        
                total_belanja += daftar_barang[data]
                print("total belanja: ", total_belanja)
                send_text("dashboard-text", "Scan berhasil, produk {} Rp{}, \nTotal belanja anda Rp{}".format(data, daftar_barang[data], total_belanja))
                #time.sleep(0.1)
            
    # Below will display the live camera
    cv2.imshow("QR Detector",resize_image)
    cv2.moveWindow("QR Detector", 400, 400)
    
    # 4. Jika sudah selesai belanja, klik tombol Bayar di Ubidots lalu tap kartu
    payProduct = get_var("pay-status-button")
    if (payProduct):
        send_text("dashboard-text", "Silahkan lakukan pembayaran! Total belanja anda, {}".format(total_belanja))
        tap_update_saldo(total_belanja) # 5. Tap kartu untuk bayar
        
        cap.release()
        cv2.destroyAllWindows()
        return False
    
    #At any point if you want to stop the Code all you need to do is press 'q' on your keyboard
    if(cv2.waitKey(1) == ord("q")):
        cap.release()
        cv2.destroyAllWindows()
