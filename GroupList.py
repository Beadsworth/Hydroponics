from Groups import Group, SuperLight, FloodZone
from ComponentList import control1, control2, control3, inlet1, outlet1, pump1, level1, white1, white2

zone1 = FloodZone(control1, inlet1, outlet1, pump1, level1, 'zone1')
zone2 = FloodZone(control2, inlet1, outlet1, pump1, level1, 'zone2')
zone3 = FloodZone(control3, inlet1, outlet1, pump1, level1, 'zone3')
light1 = SuperLight(white1, white2, 'light1')

if __name__ == '__main__':

    pass
