import os
os.system('cls')
import time
import math
import datetime

import pytz
import schedule
from scrapper import scrapper_bot
#from analyzer import link

class InvalidGMTOffsetError(ValueError):
    pass

class Timezone:
    def __init__(self, offset):
        if abs(offset) > 12:
            raise InvalidGMTOffsetError("Invalid GMT offset. Offset must be between -12 and 12.")
        self.offset = offset

    def __str__(self):
        if self.offset >= 0:
            return f"Etc/GMT+{str(self.offset)}"
        else:
            return f"Etc/GMT{str(self.offset)}"

def schedule_jobs(timezone):
    tz = pytz.timezone(str(timezone))
    # Schedule to run at 6AM UTC
    schedule.every().day.at("17:26", tz).do(scrapper_bot.scrape_wikipedia) # 6:00

    # Schedule to run at 6:10AM UTC
    #schedule.every().day.at("6:10", tz).do(link.link_data)

    while True:
        schedule.run_pending()
        time.sleep(60) # 60

try:
    timezone = Timezone(0)
    schedule_jobs(timezone)
except InvalidGMTOffsetError as e:
    print(f"Error: {str(e)}")
