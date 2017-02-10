import System
import config.HydroGroupList as HydroGroups

hydro = System.ArduinoSystem(HydroGroups.mega_controller, 'Hydroponics_System')
hydro.add_group(HydroGroups.zone1)


if __name__ == '__main__':
    pass
