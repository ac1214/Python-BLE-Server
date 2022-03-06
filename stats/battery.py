from service import Application, Service, Characteristic, Descriptor
from util.util import read_value

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 3000


# class BatteryService(Service):
#     BATTERY_SERVICE_UUID = "1000"

#     def __init__(self, index):
#         self.farenheit = True

#         Service.__init__(self, index, self.BATTERY_SERVICE_UUID, True)
#         self.add_characteristic(BatteryCharacteristic(self))


class BatteryCharacteristic(Characteristic):
    TEMP_CHARACTERISTIC_UUID = "1001"

    def __init__(self, service):
        self.notifying = False

        Characteristic.__init__(
            self, self.TEMP_CHARACTERISTIC_UUID,
            ["notify", "read"], service)

    def set_battery_callback(self):
        if self.notifying:
            value = self.get_battery_life()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        return self.notifying

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
        return read_value("battery-precent")
