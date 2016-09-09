#!/usr/bin/env python

import serial
import time

START_PACKET          = bytes.fromhex('E0')
END_PACKET            = bytes.fromhex('E1')
ACK_PACKET            = bytes.fromhex('E2')
FAIL_PACKET           = bytes.fromhex('E3')
COMMAND_PACKET        = bytes.fromhex('E4')
QUERY_PACKET          = bytes.fromhex('E5')
BAD_PIN_PACKET        = bytes.fromhex('E6')
BAD_MESSAGE_PACKET    = bytes.fromhex('E7')
TIMEOUT_ERR_PACKET    = bytes.fromhex('E8')



#    states
state = {
'RELAY_ON' : 0x00,
'RELAY_OFF' : 0x01
}
#    /states

#    messages
START_MESSAGE = bytes.fromhex('E0 E0 E0 E0 E1')
ACK_MESSAGE = bytes.fromhex('E0 E2 E2 E2 E1')
TEST_MESSAGE = bytes.fromhex('E0 E4 0C 01 E1')
saved_report = TEST_MESSAGE
#    /messages





arduino = serial.Serial(port = '/dev/ttyACM0', baudrate=9600, timeout=20)

def action(pin, state):
# failure = False --> action completed successfully
# failure = True --> action DID NOT complete successfully
# action() will return True if comm. cannot be completed within 5 tries    

# make sure pin/state are valid
    failure = True
    attempts = 5

    while (failure == True) and (attempts > 0):
        failure = initTask()
        if failure:
            attempts = attempts - 1
            continue
        failure = sendCommand(pin, state)
        if failure:
            attempts = attempts - 1            
            continue
        return failure

def initTask():
    
    arduino.reset_input_buffer()
    arduino.write(START_MESSAGE)
    arduino.flush()
    response = arduino.read(5)
    
    interpretResponse(report)    # print response on terminal
    
    if response != ACK_MESSAGE:
        #print failure type
        return True    # failure = True
    else:
        return False   # failure = False, good message was received

def sendCommand(n_pin, n_state):
       
    outbound = START_PACKET, FAIL_PACKET, int(n_pin), int(n_state), END_PACKET
    outbound_bytes = bytes(outbound)
    report_check_bytes = outbound_bytes

    arduino.reset_input_buffer()
    arduino.write(outbound_bytes)
    arduino.flush()
    report = arduino.read(5)
    
    interpretResponse(report)    # print response on terminal
    
    if report != report_check_bytes:
        return True    #failure = True, bad message was received
    return False   #failure = False, good message was received



def sendBinary(hex_string):
    
    outbound = bytes.fromhex(hex_string)

    arduino.reset_input_buffer()
    arduino.write(outbound)
    arduino.flush()
    
    report = arduino.read(5)

    interpretResponse(report)    # print response on terminal


def interpretResponse(response_bytes):
    
    print("Raw response : " + str(response_bytes))
    
    print("Response : ", end="")
    
    if response_bytes == ACK_MESSAGE :    # acknowledgement
        print("Acknowledged\n")
        return
    if (response_bytes[0] == START_PACKET[0]) and (response_bytes[1] == COMMAND_PACKET[0]) and (response_bytes[4] == END_PACKET[0]):    #command report   
        print("Pin " + str(response_bytes[2]) + " set to state " + str(response_bytes[3]) + "successfully\n")   
        return
    if (response_bytes[0] == START_PACKET[0]) and (response_bytes[1] == FAIL_PACKET[0]) and (response_bytes[3] == FAIL_PACKET[0]) and (response_bytes[4] == END_PACKET[0]) :    #failure report   
        if response_bytes[2] == BAD_PIN_PACKET[0]:    #bad pin
            print("Bad pin: " + str(response_bytes[2]) +"\n")
            return
        if response_bytes[2] == BAD_MESSAGE_PACKET[0]:    #bad message
            print("Bad message \n")
            return
        if response_bytes[2] == TIMEOUT_ERR_PACKET[0]:    #timeout
            print("Timeout error: \n")
            return
    print("Unknown response \n")    # catch-all unknown error
    return

def testBinary(input_string):
    binary_input = bytes.fromhex(input_string)
    print("Raw binary input : " + str(binary_input))
    sendBinary(input_string)
    print("Done. \n")

pause_time = 0


def onOff(pin):
    action(pin,1)
    time.sleep(pause_time)
    action(pin,0)
    time.sleep(pause_time)   

def cycle(loops):
    
    
    for i in range(loops):
        for i in range(2,10):
            onOff(i)
           
    
if __name__ == '__main__':
    
    time.sleep(3)
    
    while True:
        user_input = input('Command: ')
        testBinary(user_input)




  

