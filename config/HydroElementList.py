import ArduinoElements


# controller info
addr = '/dev/ttyACM0'
hydro_mega = ArduinoElements.Controller(addr, board_type='mega')

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

OVERFLOW_LEVEL_PIN = 34
STATUS_LEVEL_PIN = 32

# RelayBoards
box_board = ArduinoElements.RelayBoard(hydro_mega, BOX_BOARD_PIN, 'box_board')
plug_board = ArduinoElements.RelayBoard(hydro_mega, PLUG_BOARD_PIN, 'plug_board')

#  Loads
box1 = ArduinoElements.Relay(hydro_mega, BOX1_PIN, 'box1')
box2 = ArduinoElements.Relay(hydro_mega, BOX2_PIN, 'box2')
box3 = ArduinoElements.Relay(hydro_mega, BOX3_PIN, 'box3')
box4 = ArduinoElements.Relay(hydro_mega, BOX4_PIN, 'box4')
box5 = ArduinoElements.Relay(hydro_mega, BOX5_PIN, 'box5')
box6 = ArduinoElements.Relay(hydro_mega, BOX6_PIN, 'box6')
box7 = ArduinoElements.Relay(hydro_mega, BOX7_PIN, 'box7')
box8 = ArduinoElements.Relay(hydro_mega, BOX8_PIN, 'box8')

plug1 = ArduinoElements.Relay(hydro_mega, PLUG1_PIN, 'plug1')
plug2 = ArduinoElements.Relay(hydro_mega, PLUG2_PIN, 'plug2')
plug3 = ArduinoElements.Relay(hydro_mega, PLUG3_PIN, 'plug3')
plug4 = ArduinoElements.Relay(hydro_mega, PLUG4_PIN, 'plug4')

overflow_level = ArduinoElements.DigitalSensor(hydro_mega, OVERFLOW_LEVEL_PIN, 'overflow_sensor')
status_level = ArduinoElements.DigitalSensor(hydro_mega, STATUS_LEVEL_PIN, 'status_sensor')


if __name__ == '__main__':
    pass
