import dbus
import json

from advertisement import Advertisement
from service import Application, Service, Characteristic, Descriptor

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 3000
CONFIG_FILE_PATH = "config.json"

class BikeAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("BoostBike")
        self.include_tx_power = True

class BatteryService(Service):
    BATTERY_SERVICE_UUID = "00001000-0000-1000-8000-00805F9B34FB"

    def __init__(self, index):
        self.farenheit = True

        Service.__init__(self, index, self.BATTERY_SERVICE_UUID, True)
        self.add_characteristic(BatteryCharacteristic(self))
        # self.add_characteristic(UnitCharacteristic(self))

class BatteryCharacteristic(Characteristic):
    TEMP_CHARACTERISTIC_UUID = "00001001-0000-1000-8000-00805F9B34FB"

    def __init__(self, service):
        self.notifying = False

        Characteristic.__init__(
                self, self.TEMP_CHARACTERISTIC_UUID,
                ["notify", "read"], service)
        # self.add_descriptor(TempDescriptor(self))

    def get_battery_life(self):       
        with open(CONFIG_FILE_PATH, 'r') as f:
            data = json.load(f)
            precent = data["battery-precent"]

        return [dbus.Byte(precent)]

    # def set_battery_callback(self):
    #     if self.notifying:
    #         value = self.get_battery_life()
    #         self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

    #     return self.notifying

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = self.get_battery_life()
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.set_battery_callback)

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        value = self.get_battery_life()

        return value

# class TempDescriptor(Descriptor):
#     TEMP_DESCRIPTOR_UUID = "2901"
#     TEMP_DESCRIPTOR_VALUE = "CPU Temperature"

#     def __init__(self, characteristic):
#         Descriptor.__init__(
#                 self, self.TEMP_DESCRIPTOR_UUID,
#                 ["read"],
#                 characteristic)

#     def ReadValue(self, options):
#         value = []
#         desc = self.TEMP_DESCRIPTOR_VALUE

#         for c in desc:
#             value.append(dbus.Byte(c.encode()))

#         return value

# class UnitCharacteristic(Characteristic):
#     UNIT_CHARACTERISTIC_UUID = "00000003-710e-4a5b-8d75-3e5b444bc3cf"

#     def __init__(self, service):
#         Characteristic.__init__(
#                 self, self.UNIT_CHARACTERISTIC_UUID,
#                 ["read", "write"], service)
#         self.add_descriptor(UnitDescriptor(self))

#     def WriteValue(self, value, options):
#         val = str(value[0]).upper()
#         if val == "C":
#             self.service.set_farenheit(False)
#         elif val == "F":
#             self.service.set_farenheit(True)

#     def ReadValue(self, options):
#         value = []

#         if self.service.is_farenheit(): val = "F"
#         else: val = "C"
#         value.append(dbus.Byte(val.encode()))

#         return value

# class UnitDescriptor(Descriptor):
#     UNIT_DESCRIPTOR_UUID = "2901"
#     UNIT_DESCRIPTOR_VALUE = "Temperature Units (F or C)"

#     def __init__(self, characteristic):
#         Descriptor.__init__(
#                 self, self.UNIT_DESCRIPTOR_UUID,
#                 ["read"],
#                 characteristic)

#     def ReadValue(self, options):
#         value = []
#         desc = self.UNIT_DESCRIPTOR_VALUE

#         for c in desc:
#             value.append(dbus.Byte(c.encode()))

#         return value

app = Application()
app.add_service(BatteryService(0))
app.register()

adv = BikeAdvertisement(0)
adv.register()

try:
    app.run()
except KeyboardInterrupt:
    app.quit()
