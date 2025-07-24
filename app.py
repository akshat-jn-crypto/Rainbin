import serial
import time
import cv2
from ultralytics import YOLO

#Setup the communication with the microcontroller 

serialaddress = '/dev/tty.usbmodem1101'
# serialaddress = input('usbModem : ')
SerialObj = serial.Serial(serialaddress)                # COMxx  format on Windows
                                                        # ttyUSBx format on Linux
SerialObj.baudrate = 9600                             
SerialObj.bytesize = 8                                 
SerialObj.parity  = 'N'                                  
SerialObj.stopbits = 1                                  
time.sleep(3)


def send_message(message, retry=0):
    global SerialObj

    try:
        SerialObj.write(bytes(message, 'utf8'))
    except Exception as e:
        if str(e) == "write failed: [Errno 6] Device not configured":
            time.sleep(1)
            if retry > 5:
                print("Failed to send message after 5 retries")
                return
            time.sleep(1)
            SerialObj = serial.Serial(serialaddress, 1)
            send_message(message)
        else:
            print("Error in sending message : ", e)
        
    time.sleep(1)

# AI Part for object detection

#load the model
model = YOLO("best.pt")

def captureAndDetectObjects(confidence_req):
    # Capture image from camera
    cap = cv2.VideoCapture(0)
    time.sleep(0.5)
    ret, frame = cap.read()
    items = []

    if ret:
        # Save the captured image
        image_path = "captured_image.jpg"
        cv2.imwrite(image_path, frame)
        
        results = model.predict(image_path)[0]
        classes_names = results.names
        # results.show()
        for box in results.boxes:
            if box.conf[0] > confidence_req :
                items.append(classes_names[int(box.cls[0])])
    # Release the camera
    cap.release()

    return items

# To take the objects and decide dry or wet 
# Assign 1 for wet and 0 for dry
objects = {
    'bottle' : 0,
    'peels' : 1,
}

# Get the objects and store in a list of 0s and 1s
# 0 for dry and 1 for wet
def getDryWet():
    dryWet = []
    for i in captureAndDetectObjects(0.4):
        dryWet.append(objects[i])

    # if there is wet waste in the objects, throw the complete thing into the wet bin to prevent contamination of recyclables
    if 1 in dryWet:
        return 1
    if 0 in dryWet:
        return 0
    else :
        return 'NA'


while True:
    # Get the dry wet status
    dryWet = getDryWet()
    
    if dryWet == 'NA':
        print("No objects detected")
        send_message('c')
        continue

    # Send the message to the microcontroller
    send_message(['l', 'r'][dryWet])
    print(['Dry', 'Wet'][dryWet])
    # Wait for 5 seconds
    time.sleep(2)
    send_message('c')
    time.sleep(2)

    