# REAPR - Reporting Events, Anomalous Phenomena and Requests
#
# Read chat from YouTube Live Stream and save a copy when
#      keywords are used such as #EVENT: #REQUEST: #THOUGHT:
# Created as a PoC to an idea presented by Erik Bard allowing
#      for quick, easy collection of data based on observations
#      watching the Skinwalker Insiders Live Stream.
# Contributing Insiders:
#      Robert Davies <robert.kris.davies@gmail.com>, Insider Discord
#      @johns67467 - Insider Discord
#      @We Have Fun - Kris - Insider Discord

import sys
import time
import pytchat
import logging
import get_streamID
import mechanize
import re
from bs4 import BeautifulSoup
from settings import s_login, s_password
import urllib.request as urllib2
import http.cookiejar as cookielib

print("Starting REAPR - Reporting Events, Anomalous Phenomena and Requests")

logging.basicConfig(level=logging.ERROR)
log = logging.getLogger()
#YouTube_ID = " ".join(sys.argv[1:])
YouTube_ID = get_streamID.get_streamID()

def get_streamID():
    user_agent = [('User-agent','Mozilla/5.0 (X11;U;Linux 2.4.2.-2 i586; en-us;m18) Gecko/200010131 Netscape6/6.01')]

    cj = cookielib.CookieJar()
    br = mechanize.Browser()
    br.set_cookiejar(cj)
    br.set_handle_robots(False)
    br.addheaders=user_agent
    br.open("https://skinwalker-ranch.com/ranch-webcam-livestream/")

    br.select_form(nr=0)
    br.form['log'] = s_login
    br.form['pwd'] = s_password
    br.submit()

    soup = BeautifulSoup(br.response().read(), features="html5lib")
    for item in soup.find_all('iframe'):
        if 'embed' in item.get('src'):
            stream_url = item.get('src')

    stream_ID = stream_url.strip("https://www.youtube.com/live_chat?v=")
    print(stream_ID[:11])
    return stream_ID[:11]

def SWR_YT_MSG(YT_Tag, YT_DateTime, YT_User, YT_Msg):
    # Contributed by johns67467
    # depends on what DB is being used.
    import pyodbc
    from settings import db_server, db_user, db_passwd, db_name

    # Used for MySQL commands and connections
    import pymysql

    conn = pymysql.connect(host=db_server,user=db_user,passwd=db_passwd,db=db_name)
    cursor = conn.cursor()
    SWR_YT_Entry = "INSERT INTO yt_events (YT_Tag, YT_DateTime, YT_User, YT_msg) VALUES (%s, %s, %s, %s)"

    cursor.execute(SWR_YT_Entry,(YT_Tag, YT_DateTime, YT_User, YT_Msg))
    conn.commit()

def map_tags_dict(test_case: str = None):
    tag_types = {
    '#EVENT:': event_function,
    '#THOUGHT:': thought_function,
    '#REQUEST:': request_function,
    '#ALERT:': alert_function,
    }

    # Call the mapping function based on test_case as key
    tag_types[tag_type]()

def read_chat(YouTube_ID):
    chat = pytchat.create(video_id="https://www.youtube.com/watch?v=" + YouTube_ID)
    while chat.is_alive():
        for c in chat.get().sync_items():
            # Lets read all chat if we set logging to INFO
            logging.info(f"{c.datetime} [{c.author.name}]- {c.message}")
            YT_DateTime=c.datetime
            YT_User=c.author.name
            YT_Msg=c.message
            # See tag, label it ship it off
            if c.message.startswith(('#EVENT:')):
                YT_Tag='EVENT'
                SWR_YT_MSG(YT_Tag, YT_DateTime, YT_User, YT_Msg)
                print(f"EVENT: {c.datetime} [{c.author.name}] {c.message}")
            elif c.message.startswith(('#REQUEST:')):
                YT_Tag='REQUEST'
                SWR_YT_MSG(YT_Tag, YT_DateTime, YT_User, YT_Msg)
                print(f"REQUEST: {c.datetime} [{c.author.name}] {c.message}")
            elif c.message.startswith(('#THOUGHT:')):
                YT_Tag='THOUGHT'
                SWR_YT_MSG(YT_Tag, YT_DateTime, YT_User, YT_Msg)
                print(f"THOUGHT: {c.datetime} [{c.author.name}] {c.message}")
            elif c.message.startswith(('#ALERT:')):
                YT_Tag='ALERT'
                SWR_YT_MSG(YT_Tag, YT_DateTime, YT_User, YT_Msg)
                print(f"ALERT: {c.datetime} [{c.author.name}] {c.message}")
                # I would like to add some way to email this off as an ALERT!
            # There has to be some way to indicate chat is not alive anymore and reset
            elif not chat.is_alive:
                print("NOT is_alive caught.")
                main(YouTube_ID)

def main(YouTube_ID):
    try:
        read_chat(YouTube_ID)
        sys.exit(1)
    except:
        print("*** TIMEOUT ***")
        time.sleep(1)
        read_chat(YouTube_ID)
        pass
YouTube_ID=get_streamID()[:11]
main(YouTube_ID)
