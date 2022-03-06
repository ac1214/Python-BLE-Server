from service import Application, Service, Characteristic, Descriptor
from util.util import read_value, write_value

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 3000


class HeadlightService(Service):
    HEADLIGHT_SERVICE_UUID = "2000"

    def __init__(self, index):
        self.farenheit = True

        Service.__init__(self, index, self.HEADLIGHT_SERVICE_UUID, True)
        self.add_characteristic(HeadlightCharacteristic(self))


class HeadlightCharacteristic(Characteristic):
    HEADLIGHT_CHARACTERISTIC_UUID = "2001"

    def __init__(self, service):
        self.notifying = False

        Characteristic.__init__(
            self, self.HEADLIGHT_CHARACTERISTIC_UUID,
            ["notify", "read", "write"], service)

    def WriteValue(self, value, options):
        write_value("headlight", value)

    def set_headlight_callback(self):
        if self.notifying:
            value = read_value("headlight")
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = read_value("headlight")
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.set_headlight_callback)

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        return read_value("headlight")
