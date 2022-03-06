from service import Application, Service, Characteristic, Descriptor
from util.util import read_value

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 3000


class SpeedService(Service):
    SPEED_SERVICE_UUID = "1030"

    def __init__(self, index):
        self.farenheit = True

        Service.__init__(self, index, self.SPEED_SERVICE_UUID, True)
        self.add_characteristic(SpeedCharacteristic(self))


class SpeedCharacteristic(Characteristic):
    SPEED_CHARACTERISTIC_UUID = "1031"

    def __init__(self, service):
        self.notifying = False

        Characteristic.__init__(
            self, self.SPEED_CHARACTERISTIC_UUID,
            ["notify", "read"], service)

    def set_speed_callback(self):
        if self.notifying:
            value = read_value("speed")
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = read_value("speed")
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.set_speed_callback)

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        return read_value("speed")
