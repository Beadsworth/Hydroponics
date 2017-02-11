import System
import config.HydroGroupList as HydroGroups
import config.HydroComponentList as HydroComponents
import Trigger

hydro = System.ArduinoSystem(HydroGroups.mega_controller, 'Hydroponics_System')
hydro.add_group(HydroGroups.zone1)

scheduled_tasks = [
    Trigger.Schedule.every_hour(HydroGroups.zone1, 'FILL', HydroComponents.hydro_clock, '00:00:00'),
    Trigger.Schedule.every_hour(HydroGroups.zone1, 'IDLE', HydroComponents.hydro_clock, '00:10:00'),
    Trigger.Schedule.every_hour(HydroGroups.zone1, 'DRAIN', HydroComponents.hydro_clock, '00:20:00'),
    Trigger.Schedule.every_hour(HydroGroups.zone1, 'FILL', HydroComponents.hydro_clock, '00:30:00'),
    Trigger.Schedule.every_hour(HydroGroups.zone1, 'IDLE', HydroComponents.hydro_clock, '00:40:00'),
    Trigger.Schedule.every_hour(HydroGroups.zone1, 'DRAIN', HydroComponents.hydro_clock, '00:50:00'),
]

for task in scheduled_tasks:
    hydro.add_trigger(task)


if __name__ == '__main__':
    pass
