from service import Application, Service, Characteristic, Descriptor
from util.util import read_value

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 3000


class TripService(Service):
    TRIP_SERVICE_UUID = "1010"

    def __init__(self, index):
        self.farenheit = True

        Service.__init__(self, index, self.TRIP_SERVICE_UUID, True)
        self.add_characteristic(TimeCharacteristic(self))


class TimeCharacteristic(Characteristic):
    TIME_CHARACTERISTIC_UUID = "1011"

    def __init__(self, service):
        self.notifying = False

        Characteristic.__init__(
            self, self.TIME_CHARACTERISTIC_UUID,
            ["notify", "read"], service)

    def set_time_callback(self):
        if self.notifying:
            value = read_value("time-used")
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = read_value("time-used")
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.set_time_callback)

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        return read_value("time-used")


class DistanceCharacteristic(Characteristic):
    DISTANCE_CHARACTERISTIC_UUID = "1012"

    def __init__(self, service):
        self.notifying = False

        Characteristic.__init__(
            self, self.DISTANCE_CHARACTERISTIC_UUID,
            ["notify", "read"], service)

    def set_battery_callback(self):
        if self.notifying:
            value = read_value("distance-travelled")
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = read_value("distance-travelled")
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.set_battery_callback)

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        return read_value("distance-travelled")
