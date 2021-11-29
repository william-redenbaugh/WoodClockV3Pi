from RPLCD.i2c import CharLCD
import time
import re
import argparse
from datetime import datetime
import pytz


from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

def main():
        serial = spi(port=0, device=0, gpio=noop())
        device = max7219(serial, cascaded=4, block_orientation=-90,
                         rotate=0, blocks_arranged_in_reverse_order=False)

        lcd = CharLCD('PCF8574', 0x27)

        while(True):
                now = datetime.now(pytz.timezone('America/Vancouver'))
                current_time = "The Time Is: " +  now.strftime("%H:%M:%S")
                lcd.clear()
                lcd.write_string(current_time)
                show_message(device, current_time, fill="white", font=proportional(CP437_FONT))
                time.sleep(7)


main()