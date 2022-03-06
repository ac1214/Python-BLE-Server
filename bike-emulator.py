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
from userconfig.pas import PASService

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 3000


class BikeAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("BoostBike")
        self.include_tx_power = True

app = Application()
app.add_service(DiagnosticService(0))
app.add_service(BatteryService(1))
app.add_service(TripService(2))
app.add_service(RangeService(3))
app.add_service(SpeedService(4))
app.add_service(HeadlightService(5))
app.add_service(PASService(6))

app.register()

adv = BikeAdvertisement(0)
adv.register()

try:
    app.run()
except KeyboardInterrupt:
    app.quit()
