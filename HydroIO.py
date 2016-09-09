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
UNKNOWN_ERR_PACKET     = bytes.fromhex('E9')


#    states
RELAY_ON     = 0
RELAY_OFF    = 1
VALVE_OPEN = 0
VALVE_CLOSED = 1
#    /states

#    hex message strings
START_MESSAGE = 'E0 E0 E0 E0 E1'
ACK_MESSAGE = 'E0 E2 E2 E2 E1'
#    /hex message strings





arduino = serial.Serial(port = '/dev/ttyACM0', baudrate=9600, timeout=20)


def triggerSafeMode():
# trigger the safe mode by sending invalid message 5 times
# status[0] == True --> received bad message response, safeMode() successfully engaged
    
    
    for i in range(6):
        response = sendBinary('E3 E3 E3 E3 E3')    # send bad message 5 times to trigger safe state
        status = interpretResponse(response)
        time.sleep(0.01)
        if(status[1] != BAD_MESSAGE_PACKET):
            print("Unexpected arduino behavior!")
            return (False, UNKNOWN_ERR_PACKET)
            
    print("Safemode triggered successfully!")
    return (True, BAD_MESSAGE_PACKET)



def getPin(n_pin):
# success = True --> action completed successfully
# success = False --> action DID NOT complete successfully
# getPin() is just setPin() with n_state = QUERY_PACKET
# arduino will handle QUERY_PACKET and do a read-only

    n_state = 229    # intToHexString will convert to 'E5', the QUERY_PACKET
    status = setPin(n_pin, n_state)
    return status



def setPin(n_pin, n_state):
# success = True --> action completed successfully
# success = False --> action DID NOT complete successfully
# setPin() will return False if comm. cannot be completed within 5 tries    

# make sure pin/state are valid

# response[0] = True/False
# response[1] = byte_string
    success = False
    attempts = 5
   
    while not success and attempts > 0:
        response = initTask()
        success = response[0]
        if not success:
            attempts = attempts - 1
            continue
        response = sendCommand(n_pin, n_state)
        success = response[0]
        if not success:
            attempts = attempts - 1            
            continue
    
    if not success:    # still failed after while loop -> timeout
        print("Error from arduino!")
        status = (False, TIMEOUT_ERR_PACKET)
    else:
        status = interpretResponse(response[1])
            
    return status


def initTask():
    
    response = sendBinary(START_MESSAGE)
    if response != bytes.fromhex(ACK_MESSAGE):
        return [False, response]    # success = False
    else:
        return [True, response]   # success = True, good message was received

def sendCommand(n_pin, n_state):
       
    n_pin_hex_string = intToHexString(n_pin)
    n_state_hex_string = intToHexString(n_state)

    hex_string = 'E0 E4 ' + n_pin_hex_string + ' ' + n_state_hex_string + ' E1'
    report_check_bytes = bytes.fromhex(hex_string)

    response = sendBinary(hex_string)
    if (response != bytes.fromhex(hex_string)) and (n_state != 229):    # make exception for QUERY_PACKET, if statement executes if neither condition is met
        return [False, response]    #success = False, bad message was received
    return [True, response]   #success = True, good message was received



def sendBinary(hex_string):
    # accept hex string, send Binary message, print responses
    
    print("Request  : " + hex_string)
    outbound = bytes.fromhex(hex_string)

    arduino.reset_input_buffer()
    arduino.write(outbound)
    arduino.flush()
    
    response = arduino.read(5)
    print("Response: " + str(response))
    return response


def interpretResponse(response_bytes):
    # returns tuple of bytes (pass/fail, pin_state or err_type)
    # pass = ACK_PACKET
    # fail = FAIL_PACKET
    # pin_state located at response[3]
    # err_type located at response[2]
    # acknowledgement returns False; request hasn't been completed yet!
    print("Message : ", end="")
    
    if response_bytes == bytes():    # if response is empty
        print("Empty!\n")
        return (False , UNKNOWN_ERR_PACKET)    # handle empty response
    if response_bytes == bytes.fromhex(ACK_MESSAGE) :    # acknowledgement
        print("Acknowledged\n")
        return (False , ACK_PACKET)    #acknowledgement only, request not completed!
    if (response_bytes[0] == START_PACKET[0]) and (response_bytes[1] == COMMAND_PACKET[0]) and (response_bytes[4] == END_PACKET[0]):    #command report   
        print("Pin " + str(response_bytes[2]) + " in state " + str(response_bytes[3]) + "\n")   
        return (True, response_bytes[3])    # request has finished and pin state is returned
    if (response_bytes[0] == START_PACKET[0]) and (response_bytes[1] == FAIL_PACKET[0]) and (response_bytes[3] == FAIL_PACKET[0]) and (response_bytes[4] == END_PACKET[0]) :    #failure report   
        if response_bytes[2] == BAD_PIN_PACKET[0]:        #bad pin
            print("Bad pin: " + str(response_bytes[2]) +"\n")
            return (False, BAD_PIN_PACKET)
        if response_bytes[2] == BAD_MESSAGE_PACKET[0]:    #bad message
            print("Bad message \n")
            return (False, BAD_MESSAGE_PACKET)
        if response_bytes[2] == TIMEOUT_ERR_PACKET[0]:    #timeout
            print("Timeout error: \n")
            return (False, TIMEOUT_ERR_PACKET)
    print("Unknown response \n")    # catch-all unknown error
    return (False, UNKNOWN_ERR_PACKET)


def intToHexString(integer):
    if (integer >255) or (integer < 0):
        return '-1' 
    
    string = "0%X" % integer # => 0xFF
    
    if integer < 16:
        return string
    return string[1:]






pause_time = 0


def onOff(pin):
    setPin(pin,1)
    time.sleep(pause_time)
    setPin(pin,0)
    time.sleep(pause_time)   

def cycle(loops):
    
    
    for i in range(loops):
        for j in range(2,10):
            onOff(j)
            
    
if __name__ == '__main__':
    
    time.sleep(3)
    
    cycle(5)
    


    
