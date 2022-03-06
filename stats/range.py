from service import Application, Service, Characteristic, Descriptor
from util.util import read_value

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 3000


class RangeService(Service):
    RANGE_SERVICE_UUID = "1020"

    def __init__(self, index):
        self.farenheit = True

        Service.__init__(self, index, self.RANGE_SERVICE_UUID, True)
        self.add_characteristic(RangeCharacteristic(self))


class RangeCharacteristic(Characteristic):
    SPEED_CHARACTERISTIC_UUID = "1021"

    def __init__(self, service):
        self.notifying = False

        Characteristic.__init__(
            self, self.SPEED_CHARACTERISTIC_UUID,
            ["notify", "read"], service)

    def set_range_callback(self):
        if self.notifying:
            value = read_value("range")
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = read_value("range")
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.set_range_callback)

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        return read_value("range")
