#!/usr/bin/env python
# imports
from Elements import Controller, RelayBoard, Relay

# general definitions
FLOOD_TIME = 0
DRAIN_TIME = 0

# controller info
addr = '/dev/ttyACM0'
ard = Controller(addr)

# define pin locations
BOX_BOARD_PIN = 36
BOX1_PIN = 52
BOX2_PIN = 50
BOX3_PIN = 48
BOX4_PIN = 46
BOX5_PIN = 44
BOX6_PIN = 42
BOX7_PIN = 40
BOX8_PIN = 38

PLUG_BOARD_PIN = 45
PLUG1_PIN = 47
PLUG2_PIN = 49
PLUG3_PIN = 53
PLUG4_PIN = 51

# RelayBoards
box_board = RelayBoard(ard, BOX_BOARD_PIN, 'box_board')
plug_board = RelayBoard(ard, PLUG_BOARD_PIN, 'plug_board')

#  Loads
inlet_valve = Valve(ard, BOX1_PIN, 'box1')
zone1_valve = Valve(ard, BOX2_PIN, 'box2')
outlet_valve = Valve(ard, BOX3_PIN, 'box3')
box4 = Relay(ard, BOX4_PIN, 'box4')
box5 = Relay(ard, BOX5_PIN, 'box5')
box6 = Relay(ard, BOX6_PIN, 'box6')
box7 = Relay(ard, BOX7_PIN, 'box7')
box8 = Relay(ard, BOX8_PIN, 'box8')

plug1 = Relay(ard, PLUG1_PIN, 'plug1')
pump = Relay(ard, PLUG2_PIN, 'plug2')
plug3 = Relay(ard, PLUG3_PIN, 'plug3')
plug4 = Relay(ard, PLUG4_PIN, 'plug4')

zone1 = Zone('zone1', zone1_valve, inlet_valve, outlet_valve, pump)
controllers = ard,


if __name__ == '__main__':
    pass
