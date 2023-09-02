import requests
import random
import time

TOKEN = "BBFF-XHMRGDA4NAm1euVI7G6c6fitkI1JYJ" # Assign your Ubidots Token
VARIABLE_1 = "dashboard-text" # Assign the variable label to obtain the variable value
VARIABLE_2 = "power-on"
VARIABLE_3 = "pay-status"
DEVICE_LABEL = "sic-4-phoenix29"
    
def send_text(variabel, text_data):
    payload = {
        variabel: {"value": 1, "context": {"text": text_data}},
    }
    post_request(payload)

def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("Data terkirim ke Ubidots")
    return True

def get_var(variable):
    try:
        url = "http://industrial.api.ubidots.com/"
        url = url + \
            "api/v1.6/devices/{0}/{1}/".format(DEVICE_LABEL, variable)
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        req = requests.get(url=url, headers=headers)
        data = req.json()['last_value']['value']
        
        #print(data)
        return data
    except:
        pass
