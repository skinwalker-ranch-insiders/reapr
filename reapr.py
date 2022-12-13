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
    return stream_ID[:11]

def get_data():
    ###### SQL CONNECTION ######
    from settings import db_server, db_user, db_passwd, db_name
    import mysql.connector
    connection = mysql.connector.connect(
                                host=db_server,
                                database=db_name,
                                user=db_user,
                                password=db_passwd)

    cursor = connection.cursor()
    query = ("SELECT * FROM yt_events ORDER BY id DESC")
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data

def UPDATE_DB_SS(id):
    import pyodbc
    from settings import db_server, db_user, db_passwd, db_name
    import pymysql
    conn = pymysql.connect(host=db_server,user=db_user,passwd=db_passwd,db=db_name)
    cursor = conn.cursor()
    SWR_SS_Entry = "UPDATE yt_events SET IN_SS = %s where id = %s"
    cursor.execute(SWR_SS_Entry,('Y', id))
    conn.commit()

def sync_ss():
    import pandas as pd
    import datetime
    now = datetime.datetime.now()
    month = now.strftime("%B")
    year = now.strftime("%Y")
    SHEET_TUPLE = (month, "%20", year)
    SHEET_NAME = ''.join(SHEET_TUPLE)

    from settings import SHEET_ID
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
    df = pd.read_csv(url)
    for row in get_data():
        REAPR_ID=int(row[0])
        for i in df.iloc[:, 1]:
            if str(REAPR_ID) in str(i):
                UPDATE_DB_SS(int(REAPR_ID))

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
    sync_ss()

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
            elif c.message.startswith(('#FEEDBACK:')):
                YT_Tag='FEEDBACK'
                SWR_YT_MSG(YT_Tag, YT_DateTime, YT_User, YT_Msg)
                print(f"FEEDBACK: {c.datetime} [{c.author.name}] {c.message}")
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
    except Exception as e:
        print(e)
        print("*** TIMEOUT ***")
        time.sleep(1)
        read_chat(YouTube_ID)
        pass
YouTube_ID=get_streamID()
main(YouTube_ID)
