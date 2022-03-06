import dbus

from advertisement import Advertisement
from service import Application, Service, Characteristic, Descriptor
from stats.battery import BatteryService
from diagnostic.diagnostic import DiagnosticService
from stats.trip import TripService
from stats.battery import BatteryService
from stats.range import RangeService
from stats.speed import SpeedService
from userconfig.headlight import HeadlightService

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 3000


class BikeAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("BoostBike")
        self.include_tx_power = True


# class UnitCharacteristic(Characteristic):
#     UNIT_CHARACTERISTIC_UUID = "00000003-710e-4a5b-8d75-3e5b444bc3cf"

#     def __init__(self, service):
#         Characteristic.__init__(
#             self, self.UNIT_CHARACTERISTIC_UUID,
#             ["read", "write"], service)
#         self.add_descriptor(UnitDescriptor(self))

#     def WriteValue(self, value, options):
#         val = str(value[0]).upper()
#         if val == "C":
#             self.service.set_farenheit(False)
#         elif val == "F":
#             self.service.set_farenheit(True)

#     def ReadValue(self, options):
#         value = []

#         if self.service.is_farenheit():
#             val = "F"
#         else:
#             val = "C"
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
app.add_service(DiagnosticService(0))
app.add_service(BatteryService(1))
app.add_service(TripService(2))
app.add_service(RangeService(3))
app.add_service(SpeedService(4))
app.add_service(HeadlightService(5))

app.register()

adv = BikeAdvertisement(0)
adv.register()

try:
    app.run()
except KeyboardInterrupt:
    app.quit()
