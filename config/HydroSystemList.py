import System
import config.HydroGroupList as HydroGroups
import config.HydroComponentList as HydroComponents

hydro = System.ArduinoSystem(HydroGroups.mega_controller, 'Hydroponics_System')
hydro.add_group(HydroGroups.zone1)

hydro.schedule_every_hour(HydroGroups.zone1, 'FILL', HydroComponents.hydro_clock, '00:00:00')
hydro.schedule_every_hour(HydroGroups.zone1, 'IDLE', HydroComponents.hydro_clock, '00:02:30')
hydro.schedule_every_hour(HydroGroups.zone1, 'DRAIN', HydroComponents.hydro_clock, '00:03:00')
hydro.schedule_every_hour(HydroGroups.zone1, 'FILL', HydroComponents.hydro_clock, '00:05:00')
hydro.schedule_every_hour(HydroGroups.zone1, 'IDLE', HydroComponents.hydro_clock, '00:07:30')
hydro.schedule_every_hour(HydroGroups.zone1, 'DRAIN', HydroComponents.hydro_clock, '00:08:00')

hydro.schedule_every_hour(HydroGroups.zone1, 'FILL', HydroComponents.hydro_clock, '00:10:00')
hydro.schedule_every_hour(HydroGroups.zone1, 'IDLE', HydroComponents.hydro_clock, '00:12:30')
hydro.schedule_every_hour(HydroGroups.zone1, 'DRAIN', HydroComponents.hydro_clock, '00:13:00')
hydro.schedule_every_hour(HydroGroups.zone1, 'FILL', HydroComponents.hydro_clock, '00:15:00')
hydro.schedule_every_hour(HydroGroups.zone1, 'IDLE', HydroComponents.hydro_clock, '00:17:30')
hydro.schedule_every_hour(HydroGroups.zone1, 'DRAIN', HydroComponents.hydro_clock, '00:18:00')

hydro.schedule_every_hour(HydroGroups.zone1, 'FILL', HydroComponents.hydro_clock, '00:20:00')
hydro.schedule_every_hour(HydroGroups.zone1, 'IDLE', HydroComponents.hydro_clock, '00:22:30')
hydro.schedule_every_hour(HydroGroups.zone1, 'DRAIN', HydroComponents.hydro_clock, '00:23:00')
hydro.schedule_every_hour(HydroGroups.zone1, 'FILL', HydroComponents.hydro_clock, '00:25:00')
hydro.schedule_every_hour(HydroGroups.zone1, 'IDLE', HydroComponents.hydro_clock, '00:27:30')
hydro.schedule_every_hour(HydroGroups.zone1, 'DRAIN', HydroComponents.hydro_clock, '00:28:00')

hydro.schedule_every_hour(HydroGroups.zone1, 'FILL', HydroComponents.hydro_clock, '00:30:00')
hydro.schedule_every_hour(HydroGroups.zone1, 'IDLE', HydroComponents.hydro_clock, '00:32:30')
hydro.schedule_every_hour(HydroGroups.zone1, 'DRAIN', HydroComponents.hydro_clock, '00:33:00')
hydro.schedule_every_hour(HydroGroups.zone1, 'FILL', HydroComponents.hydro_clock, '00:35:00')
hydro.schedule_every_hour(HydroGroups.zone1, 'IDLE', HydroComponents.hydro_clock, '00:37:30')
hydro.schedule_every_hour(HydroGroups.zone1, 'DRAIN', HydroComponents.hydro_clock, '00:38:00')

hydro.schedule_every_hour(HydroGroups.zone1, 'FILL', HydroComponents.hydro_clock, '00:40:00')
hydro.schedule_every_hour(HydroGroups.zone1, 'IDLE', HydroComponents.hydro_clock, '00:42:30')
hydro.schedule_every_hour(HydroGroups.zone1, 'DRAIN', HydroComponents.hydro_clock, '00:43:00')
hydro.schedule_every_hour(HydroGroups.zone1, 'FILL', HydroComponents.hydro_clock, '00:45:00')
hydro.schedule_every_hour(HydroGroups.zone1, 'IDLE', HydroComponents.hydro_clock, '00:47:30')
hydro.schedule_every_hour(HydroGroups.zone1, 'DRAIN', HydroComponents.hydro_clock, '00:48:00')

hydro.schedule_every_hour(HydroGroups.zone1, 'FILL', HydroComponents.hydro_clock, '00:50:00')
hydro.schedule_every_hour(HydroGroups.zone1, 'IDLE', HydroComponents.hydro_clock, '00:52:30')
hydro.schedule_every_hour(HydroGroups.zone1, 'DRAIN', HydroComponents.hydro_clock, '00:53:00')
hydro.schedule_every_hour(HydroGroups.zone1, 'FILL', HydroComponents.hydro_clock, '00:55:00')
hydro.schedule_every_hour(HydroGroups.zone1, 'IDLE', HydroComponents.hydro_clock, '00:57:30')
hydro.schedule_every_hour(HydroGroups.zone1, 'DRAIN', HydroComponents.hydro_clock, '00:58:00')


if __name__ == '__main__':
    pass
