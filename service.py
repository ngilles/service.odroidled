import time
import xbmc
import xbmcaddon

triggers = [
    'none', # Off
    'default-on', # On
    'heartbeat', # Heartbeat
]

led_trigger_path = '/sys/devices/gpio_leds.43/leds/blue:heartbeat/trigger'
#led_trigger_path = '/dev/null'

class SettingsMonitor(xbmc.Monitor):
    def __init__(self, settings_changed):
        xbmc.Monitor.__init__(self)
        self._settings_changed_handler = settings_changed

    def onSettingsChanged(self):
        self._settings_changed_handler()

def set_trigger(trigger):
    with open(led_trigger_path, 'w') as t:
        t.write(triggers[trigger])

if __name__ == '__main__':
    addon = xbmcaddon.Addon()

    def update_trigger():
        trigger = int(addon.getSetting('trigger'))

        if trigger >= len(triggers):
            trigger = 0

        xbmc.log('Setting trigger to: %s' % triggers[trigger], level=xbmc.LOGDEBUG)
        set_trigger(trigger)

    monitor = SettingsMonitor(update_trigger)

    xbmc.log('Starting ODROID-C2 Led control', level=xbmc.LOGDEBUG)
    update_trigger()

    # Just wait till Kodi is ready to quit
    monitor.waitForAbort()

    xbmc.log('Stopping ODROID-C2 Led control, setting trigger back to heartbeat', level=xbmc.LOGDEBUG)

    # Set back to default heartbeat
    set_trigger(2)
