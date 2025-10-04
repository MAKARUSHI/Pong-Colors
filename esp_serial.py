import serial
import json

ser = serial.Serial('COM3', 115200, timeout=0.01)

senderName = ""
c0Dvalue = {"name":"controller0", "joXVal":1937, "joYVal":1937, "joSVal":1}
c1Dvalue = {"name":"controller1", "joXVal":1937, "joYVal":1937, "joSVal":1}


def getSerialData():
    global c0Dvalue,c1Dvalue
    #currentController = c0Dvalue
    #line = ser.readline().strip()
    success = False
    while not success:
        try:
            line = ser.readline().decode('ascii').strip()
            success = True
        except:
            print("fail")
    
    if line.startswith("{") and line.endswith("}"):
        data = json.loads(line)
        
        if data.get("name", senderName) == "controller0":
            currentController = c0Dvalue

        elif data.get("name", senderName) == "controller1":
            currentController = c1Dvalue

        currentController["joXVal"] = data.get("joXVal")
        currentController["joYVal"] = data.get("joYVal")
        currentController["joSVal"] = data.get("joSVal")
    currentController = c0Dvalue
    #except (json.JSONDecodeError, UnicodeDecodeError):
        #pass
    
    return currentController
