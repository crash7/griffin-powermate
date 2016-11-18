from pywinusb.hid import HidDeviceFilter


def find_griffin_powermate():
    return GriffinPowermate.find_all()


class GriffinPowermate():
    VENDOR = 0x077d
    PRODUCT = 0x0410
    MOVE_LEFT = -1
    MOVE_RIGHT = 1

    def __init__(self, raw_device):
        self.__device = raw_device
        self.__device.set_raw_data_handler(
            lambda raw_data: self.__internal_listener(raw_data))
        self.__events = {}

    @classmethod
    def find_all(cls):
        # FixMe
        return [cls(device) for device in
                HidDeviceFilter(vendor_id=cls.VENDOR,
                                product_id=cls.PRODUCT).get_devices()]

    def __internal_listener(self, raw_data):
        """
        [0, button_status, move, 0, bright, pulse_status, pulse_value]
        """
        move = 1 if raw_data[2] < 128 else -1
        if 'move' in self.__events:
            self.__events['move'](move, raw_data[1])
        if 'raw' in self.__events:
            self.__events['raw'](raw_data)

    def is_plugged(self):
        return self.__device.is_plugged()

    def open(self):
        if not self.__device.is_opened():
            self.__device.open()

    def close(self):
        if self.__device.is_opened():
            self.__device.close()

    def on_event(self, event, callback):
        self.__events[event] = callback

    def set_brightness(self, bright):
        # alternative: device.send_output_report([0, bright])
        self.__device.send_feature_report(
            [0, 0x41, 0x01, 0x01, 0x00, bright % 255, 0x00, 0x00, 0x00])

    def set_led_pulsing_status(self, on=True):
        # led pulsing on/off
        self.__device.send_feature_report([0, 0x41, 0x01, 0x03, 0x00, 0x01
                                           if on else 0x00, 0x00, 0x00, 0x00])

    def set_led_pulsing_default(self):
        self.__device.send_feature_report(
            [0, 0x41, 0x01, 0x04, 0x00, 0x01, 0x00, 0x00, 0x00])


if __name__ == '__main__':
    from time import sleep
    from msvcrt import kbhit

    def move_listener(direction, button):
        print("Moved: {0} - {1}"
              .format('LEFT' if direction == GriffinPowermate.MOVE_LEFT
                      else 'RIGHT', button))

    def raw_listener(data):
        print "Moved: {0}".format(data)

    devices = GriffinPowermate.find_all()
    if len(devices) > 0:
        print "Found Powermates"
        powermate = devices[0]

        try:
            powermate.open()

            powermate.set_brightness(200)

            powermate.set_led_pulsing_status(True)
            powermate.set_led_pulsing_default()

            powermate.on_event('move', move_listener)
            powermate.on_event('raw', raw_listener)

            print("\nWaiting for data..."
                  "\nPress any (system keyboard) key to stop...")
            while not kbhit() and powermate.is_plugged():
                # keep the device opened to receive events
                sleep(0.5)
        finally:
            powermate.set_led_pulsing_status(False)
            powermate.set_brightness(0)
            powermate.close()
