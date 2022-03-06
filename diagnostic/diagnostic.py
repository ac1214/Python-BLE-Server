from service import Service, Characteristic
from util.util import read_value

NOTIFY_TIMEOUT = 3000


class DiagnosticService(Service):
    DIAGNOSTIC_SERVICE_UUID = "5000"

    def __init__(self, index):
        self.farenheit = True

        Service.__init__(self, index, self.DIAGNOSTIC_SERVICE_UUID, True)
        self.add_characteristic(HWVersionCharacteristic(self))
        self.add_characteristic(SWVersionCharacteristic(self))
        self.add_characteristic(FWVersionCharacteristic(self))
        self.add_characteristic(ModelCharacteristic(self))
        self.add_characteristic(BatteryTempCharacteristic(self))


class HWVersionCharacteristic(Characteristic):
    HWVERSION_CHARACTERISTIC_UUID = "5001"

    def __init__(self, service):
        Characteristic.__init__(
            self, self.HWVERSION_CHARACTERISTIC_UUID,
            ["read"], service)

    def ReadValue(self, options):
        return read_value("hw-version")


class SWVersionCharacteristic(Characteristic):
    SWVERSION_CHARACTERISTIC_UUID = "5002"

    def __init__(self, service):
        Characteristic.__init__(
            self, self.SWVERSION_CHARACTERISTIC_UUID,
            ["read"], service)

    def ReadValue(self, options):
        return read_value("sw-version")


class FWVersionCharacteristic(Characteristic):
    FWVERSION_CHARACTERISTIC_UUID = "5003"

    def __init__(self, service):
        Characteristic.__init__(
            self, self.FWVERSION_CHARACTERISTIC_UUID,
            ["read"], service)

    def ReadValue(self, options):
        return read_value("fw-version")


class ModelCharacteristic(Characteristic):
    MODEL_CHARACTERISTIC_UUID = "5004"

    def __init__(self, service):
        Characteristic.__init__(
            self, self.MODEL_CHARACTERISTIC_UUID,
            ["read"], service)

    def ReadValue(self, options):
        return read_value("model")


class BatteryTempCharacteristic(Characteristic):
    BATTERYTEMP_CHARACTERISTIC_UUID = "5005"

    def __init__(self, service):
        Characteristic.__init__(
            self, self.BATTERYTEMP_CHARACTERISTIC_UUID,
            ["read"], service)

    def ReadValue(self, options):
        return read_value("battery-temp")
