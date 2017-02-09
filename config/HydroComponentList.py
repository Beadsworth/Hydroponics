import Components
import config.HydroElementList as HydroElements

# pump and lights
pump = Components.Pump.Pump(HydroElements.plug1, 'pump')

# valves
inlet_valve = Components.Valve.Valve(HydroElements.box1, 'inlet_valve')
control1 = Components.Valve.Valve(HydroElements.box2, 'zone1_control_valve')
outlet_valve = Components.Valve.Valve(HydroElements.box3, 'outlet_valve')

# sensors
level1 = Components.WaterLevelSensor.WaterLevelSensor(HydroElements.level, 'level1')

# misc
hydro_clock = Components.Clock.Clock("clock")
twitter_account = Components.TwitterAccount.TwitterAccount("twitter")


if __name__ == '__main__':
    pass
