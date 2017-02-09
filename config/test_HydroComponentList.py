import Components
import config.test_HydroElementList as test_HydroElements

outlet1 = Components.Valve.Valve(test_HydroElements.red, 'red1')
control3 = Components.Valve.Valve(test_HydroElements.orange, 'orange1')
control2 = Components.Valve.Valve(test_HydroElements.yellow, 'yellow1')
control1 = Components.Valve.Valve(test_HydroElements.green, 'green1')
inlet1 = Components.Valve.Valve(test_HydroElements.blue, 'blue1')
pump1 = Components.Pump.Pump(test_HydroElements.purple, 'purple1')
white1 = Components.Light.Light(test_HydroElements.white1, 'white1')
white2 = Components.Light.Light(test_HydroElements.white2, 'white2')
level1 = Components.WaterLevelSensor.WaterLevelSensor(test_HydroElements.level, 'level1')

clock1 = Components.Clock.Clock("clock1")
twitter_account = Components.TwitterAccount.TwitterAccount("twitter")


if __name__ == '__main__':
    pass
