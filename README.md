# Griffin Powermate Python library for Windows

This library to use the [Griffin Powermate](https://store.griffintechnology.com/powermate) from Python in windows.

![Griffin Powermate](https://store.griffintechnology.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/n/a/na16029_powermate_1.jpg)

## Requirements
- Windows (yes, this is windows only; tested on Windows 7 x64)
- Python 2.7 (tested on 2.7.9)
- [pywinusb](https://github.com/rene-aguirre/pywinusb)
- A [Griffin Powermate](https://store.griffintechnology.com/powermate)!

## Install with pip
```pip install griffin_powermate```
```pip install pywinusb```

## Usage
```py
from griffin_powermate import GriffinPowermate
from time import sleep
from msvcrt import kbhit() # ctrl+c to exit

def move_listener(direction, button):
  print "Moved: {0} - {1}".format(direction, button)

devices = GriffinPowermate.find_all()
if len(devices) > 0:
  print "Found Powermates"
  powermate = devices[0]

  try:
    powermate.open()
    powermate.on_event('move', move_listener)

    print("\nWaiting for data...\nPress any (system keyboard) key to stop...")
    while not kbhit() and powermate.is_plugged():
      # keep the device opened to receive events
      sleep(0.5)
  finally:
    powermate.close()
```

## API
TBC

## Documentation & useful links
- [Powermate SDK API docs](https://github.com/zorbathut/powermate/blob/master/Original%20Windows%20API.zip) - Thanks @zorbathut
- [PowerMate programming in .Net – Part 2](http://thammer.net/?p=374) - By Thomas H@mmer

## Contributing
Contributions and suggestions are welcome :)

## Licence
Released under the [MIT License](LICENSE)
