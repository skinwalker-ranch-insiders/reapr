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
#      @John Neiberger - Insider Discord
import re
import sys
import time
import pytchat
import logging
import mechanize
import datetime
import mysql.connector
import http.cookiejar as cookielib
import pandas as pd
from bs4 import BeautifulSoup
from settings import s_login, s_password, db_server, db_user, db_passwd, db_name, sheet_id

def get_streamID():
    user_agent = [
        ('User-agent',
        'REAPR (X11;U;Linux MyKernelMyBusiness; Insider-Powered) Skinwalker/20221214-1 reapr.py')
        ]

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

def update_db_ss(id):
    connection = mysql.connector.connect(
                                        host=db_server,
                                        user=db_user,
                                        passwd=db_passwd,
                                        db=db_name)
    cursor = connection.cursor()
    query = "UPDATE yt_events SET IN_SS = %s where id = %s"
    cursor.execute(query,('Y', id))
    connection.commit()

def sync_ss():
    now = datetime.datetime.now()
    month = now.strftime("%B")
    year = now.strftime("%Y")
    sheet_tuple = (month, "%20", year)
    sheet_name = ''.join(sheet_tuple)

    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df = pd.read_csv(url)
    for row in get_data():
        reapr_id=int(row[0])
        for i in df.iloc[:, 1]:
            if str(reapr_id) in str(i):
                update_db_ss(int(reapr_id))

def swr_yt_msg(yt_tag, yt_datetime, yt_user, yt_msg):
    # Contributed by johns67467
    # depends on what DB is being used.
    connection = mysql.connector.connect(
                                        host=db_server,
                                        user=db_user,
                                        passwd=db_passwd,
                                        db=db_name)
    cursor = connection.cursor()
    query = "INSERT INTO yt_events (yt_tag, yt_datetime, yt_user, yt_msg) VALUES (%s, %s, %s, %s)"

    cursor.execute(query,(yt_tag, yt_datetime, yt_user, yt_msg))
    connection.commit()
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
            yt_datetime=c.datetime
            yt_user=c.author.name
            yt_msg=c.message
            # See tag, label it ship it off
            tag = re.search(r'^#\w+:', c.message.upper())

            if tag:
                yt_tag = tag[1:-1]
                if yt_tag in ['EVENT', 'REQUEST', 'THOUGHT', 'FEEDBACK']:
                    swr_yt_msg(yt_tag, yt_datetime, yt_user, yt_msg)
                    print(f"ALERT: {c.datetime} [{c.author.name}] {c.message}")
            elif not chat.is_alive:
                print("NOT is_alive caught.")
                main(youtube_id)

def main():
    print("Starting REAPR - Reporting Events, Anomalous Phenomena and Requests")
    YouTube_ID=get_streamID()

    logging.basicConfig(level=logging.ERROR)
    log = logging.getLogger()

    try:
        read_chat(YouTube_ID)
        sys.exit(1)
    except Exception as e:
        print(e)
        print("*** TIMEOUT ***")
        time.sleep(1)
        read_chat(YouTube_ID)
        pass

if __name__ == "__main__":
    main()
