from RPLCD.i2c import CharLCD
import time
import re
import argparse
from datetime import datetime
from datetime import date as Date
import pytz
from astral import LocationInfo
from astral.sun import sun

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

def main():
	serial = spi(port=0, device=0, gpio=noop())
	device = max7219(serial, cascaded=4, block_orientation=-90,rotate=0, blocks_arranged_in_reverse_order=False)
	lcd = CharLCD('PCF8574', 0x27)
	enabled = True
	while(True):

		now = datetime.now(pytz.timezone('America/Vancouver'))
		today = datetime.today()
		loc = LocationInfo(name='SJC', region='CA, USA', timezone='America/Los_Angeles',latitude=37.3713439, longitude=-121.944675)
		s = sun(loc.observer, date=Date(today.year, today.month, today.day), tzinfo=loc.timezone)

		now_unixtime = time.mktime(now.timetuple())
		sunset_unixtime = time.mktime(s["sunset"].timetuple())
		sunrise_unixtime = time.mktime(s["sunrise"].timetuple())

		if(now_unixtime < sunset_unixtime):
			enabled = False
		if(now_unixtime > sunrise_unixtime):
			enabled = True

		if enabled:
			current_time =  now.strftime("%m/%d/%Y : %H:%M:%S")
			show_message(device, current_time, fill="white", font=proportional(CP437_FONT))
		current_time = "Date And Time: " + now.strftime("%m/%d/%Y : %H:%M:%S")
		lcd.clear()
		lcd.write_string(current_time)
		time.sleep(5)
main()
