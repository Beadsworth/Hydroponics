#include <MemoryFree.h>
#include <HydroComponents3.h>
/*
 
 Slave Arduino
 
 Arduino will establish serial connection with Raspi
 and execute commands as they are received.  All scheduling
 is done on Raspi.  Arduino must only receive one command
 at a time.  Arduino will not keep time.
 
*/
 
//=================================
// load objects

#define TIMEOUT 1000
#define DEADMAN_LIMIT 900000  //time in millisec

#define OPEN HIGH
#define CLOSED LOW
#define RELAY_ON 0x00
#define RELAY_OFF 0X01


#define START_PACKET 0xE0
#define END_PACKET 0xE1
#define ACK_PACKET 0xE2
#define FAIL_PACKET 0xE3
#define COMMAND_PACKET 0xE4
#define QUERY_PACKET 0xE5
#define BAD_PIN 0xE6
#define BAD_MESSAGE 0xE7
#define TIMEOUT_ERR 0xE8

#define WAIT 0xF0
#define LISTEN 0xF1
#define EXECUTE 0xF2
#define FAIL 0xF3
#define SAFE 0xF4

byte current_mode = WAIT;
byte current_failure = TIMEOUT_ERR;

byte input_message[] = {FAIL_PACKET, FAIL_PACKET, FAIL_PACKET, FAIL_PACKET, FAIL_PACKET};
byte report_message[] = {START_PACKET, COMMAND_PACKET, ACK_PACKET, ACK_PACKET, END_PACKET};
byte ack_message[] = {START_PACKET, ACK_PACKET, ACK_PACKET, ACK_PACKET, END_PACKET};
byte fail_message[] = {START_PACKET, FAIL_PACKET, FAIL_PACKET, FAIL_PACKET, END_PACKET};




unsigned long deadman_start = millis();
unsigned long deadman_end = millis();
unsigned long deadman_diff = deadman_end - deadman_start;


bool already_in_safe_mode = false;  //only go through "enterSafeMode()" procedure if you aren't already in safe mode 


byte n_pin = 0x00;
byte n_state = 0x00;

int fail_count = 0;

//appliance objects
Load t_pump(2);
Load t_light1A(11);
Load t_light1B(12);
//Load t_light2A(13);
//Load t_light2B (13);

Load * pump = & t_pump;
Load * light1A = & t_light1A;
Load * light1B = & t_light1B;
//Load * light2A = & t_light2A;
//Load * light2B = & t_light2B;
  
//valve objects
Valve t_inlet_valve(3);
Valve t_zone1_valve(4);
Valve t_zone2_valve(5);
Valve t_zone3_valve(6);
Valve t_zone4_valve(7);
Valve t_zone5_valve(8);
Valve t_zone6_valve(9);
Valve t_outlet_valve(10);

Load * inlet_valve = & t_inlet_valve;
Load * zone1_valve = & t_zone1_valve;
Load * zone2_valve = & t_zone2_valve;
Load * zone3_valve = & t_zone3_valve;
Load * zone4_valve = & t_zone4_valve;
Load * zone5_valve = & t_zone5_valve;
Load * zone6_valve = & t_zone6_valve;
Load * outlet_valve = & t_outlet_valve;
  
Load * load_list[] = {

pump,
light1A,
light1B,
//light2A,
//light2B,
inlet_valve,
zone1_valve,
zone2_valve,
zone3_valve,
zone4_valve,
zone5_valve,
zone6_valve,
outlet_valve,

};

int load_list_size = 11;

void sendResponse(byte buffer[5]) {
  Serial.write(buffer, 5);
  Serial.flush();
  
}

void resetInputMessage(){
  input_message[0] = FAIL_PACKET;
  input_message[1] = FAIL_PACKET;
  input_message[2] = FAIL_PACKET;
  input_message[3] = FAIL_PACKET;
  input_message[4] = FAIL_PACKET;
}



void clearInputBuffer() {
  while (Serial.available()) {
    // read until empty
    Serial.read(); 
    } 
   
   resetInputMessage(); 
    
}

void printMem(){
  //Serial.print("freeMemory()=");
  //Serial.println(freeMemory());
  //Serial.flush();
}



void enterMode(byte next_mode) {
  
  //modify mode control marker, changing mode on next loop iteration
  current_mode = next_mode;  
    
}

Load * findLoad(uint8_t f_pin){
  
  for(int i = 0; i < load_list_size ; i++){
    if(load_list[i]->getPin() == f_pin){
      return load_list[i];
      
    }
  }
    
    return 0;
}



void Wait() {
  //deadman_start resets in Execute() state
  deadman_end = millis();
   
  if(deadman_start > deadman_end){  //reset if overflow
    deadman_start = deadman_end;
  }
  
  deadman_diff = deadman_end - deadman_start;
  
  if(deadman_diff > DEADMAN_LIMIT){
    enterMode(SAFE);
    digitalWrite(13, HIGH);
    return;
  }
  
  
    
  
  digitalWrite(13, LOW);
  
  
  
  
  
  
  //debug message
  //Serial.println();
  //Serial.println("Waiting...");
  
  //make sure input_message is reset
  resetInputMessage();
  //delay(500);
  //wait for "start transmission" signal
  //react to ANY incoming signal
  //valid signal starts with START-PACKET, ends with END_PACKET, and has size of 5 bytes
  
  //int buffer_size = 5;
  int buffer_size = Serial.readBytes((char *)input_message,5);
  delay(25);
  
  if(buffer_size == 0){
    return;  //do nothing
  }
  
  if( (buffer_size != 5) || (Serial.available() > 0) ){
    current_failure = BAD_MESSAGE;
    enterMode(FAIL);
    return; 
  }
  if((input_message[0] != START_PACKET) || (input_message[1] != START_PACKET) || (input_message[2] != START_PACKET)|| (input_message[3] != START_PACKET) || (input_message[4] != END_PACKET) ){
    current_failure = BAD_MESSAGE;
    enterMode(FAIL);
    return; 
  }
    
  enterMode(LISTEN);
   
    
}

void Listen() {
  //debug message
  //Serial.println();
  //Serial.println("Listening...");
  //acknowledge transmission start
  //listen for command message
  //listen mode is catch-all for signal failure
  
  //clear buffer, send acknowledgement, and delay() for response
  clearInputBuffer();  
  sendResponse(ack_message);
  
  //read buffer
  int buffer_size = Serial.readBytes((char *)input_message,5);
  delay(25);
  
  if(buffer_size == 0){
    current_failure = TIMEOUT_ERR;
    enterMode(FAIL);
    return;
  }  
  
  if( (buffer_size != 5) || (Serial.available() > 0) ){
    current_failure = BAD_MESSAGE;
    enterMode(FAIL);
    return;
  }
  
  if((input_message[0] != START_PACKET) || (input_message[1] != COMMAND_PACKET) || (input_message[4] != END_PACKET) ){
    
    current_failure = BAD_MESSAGE;
    enterMode(FAIL);
    return; 
  }
  n_pin = input_message[2];
  n_state = input_message[3];
  
  if( (n_state != 0) && (n_state != 1) && (n_state != QUERY_PACKET)){
    
    current_failure = BAD_MESSAGE;
    enterMode(FAIL);
    return;
  } 
  
  if(findLoad(n_pin) == 0){
    
    current_failure = BAD_PIN;
    enterMode(FAIL);
    return;
  }
  
  
  enterMode(EXECUTE); 
    
}

void Execute(byte c_pin, byte c_state) {
  //debug message
  //Serial.println();
  //Serial.println("Executing...");
  //send report
  //set pin state
  //enter wait mode
  
  //clear command info
  n_pin = 0x00;
  n_state = 0x00; 
  //clear buffer, send report, and delay() for response  
  Load * load = findLoad(c_pin);
  
  if(c_state != QUERY_PACKET){
    load->setState(c_state);
  } 
  int t_state = load->getState();
  byte t_state_byte = byte(t_state);
  
  
  report_message[2] = c_pin;
  report_message[3] = t_state_byte;
  clearInputBuffer();  
  sendResponse(report_message);
  //delay(100);
  //clear report message
  report_message[2] = FAIL_PACKET; 
  report_message[3] = FAIL_PACKET;
    
  
  deadman_start = millis();
  
  already_in_safe_mode = false; //reset safe mode flag -- you're out of safe state by now
  fail_count = 0;  //reset fail_count because command executed successfully
  enterMode(WAIT);
}

void Fail() {
  
  digitalWrite(13, HIGH);
  //debug message
  //Serial.println();
  //Serial.println("Failing...");
  //set failure flag
  //go back to listen mode
  
  clearInputBuffer();
  fail_message[2] = current_failure;
  sendResponse(fail_message);
  
  if(fail_count >=5){
    enterMode(SAFE);   
  }
  else{
    fail_count = fail_count + 1;
    enterMode(LISTEN); 
  }
  current_failure = TIMEOUT_ERR;
  
}

void Safe() {
  //debug message
  //Serial.println();
  //Serial.println("Saving...");
  //set components to a safe mode
  //attempt to re-establish serial connection
  fail_count = 0;
  
  if(already_in_safe_mode == false){  //don't senselessly re-enty safe mode ad infinitum
    enterSafeMode(); 
  }
  
  clearInputBuffer();
  
  enterIdleMode();  
  deadman_start = millis();
  
  
  already_in_safe_mode = true;
  
  enterMode(WAIT);
}



void initAllComponents() {
  //debug message
  //Serial.println("Initializing...");
  //initialize all load pins to OUTPUT mode
  pump->init();
  light1A->init();
  light1B->init();
  //light2A->init();
  //light2B->init(); 
  inlet_valve->init();
  zone1_valve->init();
  zone2_valve->init();
  zone3_valve->init();
  zone4_valve->init();
  zone5_valve->init();
  zone6_valve->init();
  outlet_valve->init();  
  
  //enter SAFEMODE to drain all fluids
  //enterSafeMode();
  //wait 15 minutes for fluids to drain
  //delay(15*60*1000);
  //enter idle state in preparation for commands
  //enterIdleMode();
    
}

void enterSafeMode() {
  //Safe-State shuts off appliance power
  //and allows plumbing to drain
  //no delay for drainage
    
  //turn off pump & lights
  pump->setState(OFF);
  pump->setState(OFF);
  light1A->setState(OFF);
  light1B->setState(OFF);
  //light2A->setState(OFF);
  //light2B->setState(OFF); 
  
  //OPEN all valves, allowing to drain
  outlet_valve->setState(OPEN);
  zone1_valve->setState(OPEN);
  zone2_valve->setState(OPEN);
  zone3_valve->setState(OPEN);
  zone4_valve->setState(OPEN);
  zone5_valve->setState(OPEN);
  zone6_valve->setState(OPEN);
  inlet_valve->setState(OPEN);
  
  for(int i = 0; i <= 2; i++){   //delay 2 sec
    delay(1000);
  }
  
  
  
}


void enterIdleMode() {
  
  //Wait-Mode shuts off appliance power
  //and CLOSES all valves
  
  //turn off pump & lights
  pump->setState(OFF);
  light1A->setState(OFF);
  light1B->setState(OFF);
  //light2A->setState(OFF);
  //light2B->setState(OFF); 
  
  //CLOSE all valves, allowing to drain
  inlet_valve->setState(CLOSED);
  zone1_valve->setState(CLOSED);
  zone2_valve->setState(CLOSED);
  zone3_valve->setState(CLOSED);
  zone4_valve->setState(CLOSED);
  zone5_valve->setState(CLOSED);
  zone6_valve->setState(CLOSED);
  outlet_valve->setState(CLOSED);
  
  enterMode(WAIT);
    
}

void setup() {
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  
  // initialize serial:
  Serial.begin(9600);
  Serial.setTimeout(TIMEOUT);
  
  delay(500);
  //debug message
  //Serial.println("Setup...");
  initAllComponents();
  
}

void loop() {
  //debug message
  //Serial.println();
  //Serial.println("Looping...");
  //delay(100);
  switch(current_mode) {
    case WAIT:
      Wait();
      break;
    case LISTEN:
      Listen();
      break;
    case EXECUTE:
      Execute(n_pin, n_state);
      break;
    case FAIL:
      Fail();
      break;
    case SAFE:
      Safe();
      break;
    default:
      enterMode(FAIL);
      break;
  }
  
}



