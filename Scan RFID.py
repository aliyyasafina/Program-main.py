import RPi.GPIO as GPIO
        from ubidots_get_post import *
        from mfrc522 import SimpleMFRC522

        GPIO.setwarnings(False)
        rfid = SimpleMFRC522()

        tap_success = False
        saldo = 100000

        def tap_check_saldo():
            # Read RFID saldo
            global saldo
            print("Cek saldo RFID")
            id, data = rfid.read()
            print("Saldo", id, data)
            saldo = int(data)
            # Show data in Ubidots dashboard 
            send_text("dashboard-text", "Tap berhasil, saldo anda {}".format(saldo))
            return
                
        def tap_update_saldo(total_belanja):
            saldo_akhir = saldo - total_belanja
            rfid.write(str(saldo_akhir))
            print("Saldo akhir ", saldo_akhir)

            # Show data in Ubidots dashboard 
            send_text("dashboard-text", "Pembayaran berhasil, sisa saldo anda {}".format(saldo_akhir))
            
        #tap_check_saldo()
        #tap_update_saldo()#
