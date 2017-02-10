from Components import Clock, Pump, Valve, WaterLevelSensor, TwitterAccount
import config.HydroElementList as HydroElements


# pump and lights
pump = Pump.Pump(HydroElements.plug1, 'pump')

# valves
inlet_valve = Valve.Valve(HydroElements.box1, 'inlet_valve')
control1 = Valve.Valve(HydroElements.box2, 'zone1_control_valve')
outlet_valve = Valve.Valve(HydroElements.box3, 'outlet_valve')

# sensors
level1 = WaterLevelSensor.WaterLevelSensor(HydroElements.level, 'level1')

# misc
hydro_clock = Clock.Clock("clock")
twitter_account = TwitterAccount.TwitterAccount("twitter")


if __name__ == '__main__':
    pass
