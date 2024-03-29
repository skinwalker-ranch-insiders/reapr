# REAPR - Reporting Events, Anomalous Phenomena et Requests
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
import datetime
import mechanize
import pandas as pd
import mysql.connector
import http.cookiejar as cookielib
from bs4 import BeautifulSoup
from settings import (
    s_login,
    s_password,
    db_server,
    db_user,
    db_passwd,
    db_name,
    sheet_id,
)


def get_streamID():
    """ Get current Stream ID from the YouTube channel"""
    user_agent = [
        (
            "User-agent",
            "REAPR (X11;U;Linux MyKernelMyBusiness; Insider-Powered) Skinwalker/20221214-1 reapr.py",
        )
    ]

    cj = cookielib.CookieJar()
    br = mechanize.Browser()
    br.set_cookiejar(cj)
    br.set_handle_robots(False)
    br.addheaders = user_agent
    br.open("https://skinwalker-ranch.com/ranch-webcam-livestream/")

    br.select_form(nr=0)
    br.form["log"] = s_login
    br.form["pwd"] = s_password
    br.submit()

    soup = BeautifulSoup(br.response().read(), features="html5lib")
    for item in soup.find_all("iframe"):
        if "embed" in item.get("src"):
            stream_url = item.get("src")
    """ 2023/1/23 -- strips true colors show up. I could have used ("htps:/wyoubecmlivha?=") """
    """ This makes it buggy if the streamID contains ANY of those letters. """
    #stream_ID = stream_url.strip("https://www.youtube.com/live_chat?v=")
    stream_ID = stream_url[36:]
    return stream_ID[:11]


def load_from_db():
    """Retrieve YouTube events from database"""
    connection = mysql.connector.connect(
        host=db_server, database=db_name, user=db_user, password=db_passwd
    )

    cursor = connection.cursor()
    query = "SELECT * FROM yt_events ORDER BY id DESC"
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data


def update_db_ss(id):
    """Update database to indicate when events have been pushed to spreadsheet"""
    connection = mysql.connector.connect(
        host=db_server, user=db_user, passwd=db_passwd, db=db_name
    )
    cursor = connection.cursor()
    query = "UPDATE yt_events SET IN_SS = %s where id = %s"
    cursor.execute(query, ("Y", id))
    connection.commit()
    connection.close()


def sync_ss():
    """Synchronize Google Docs Spreadsheet with event database"""
    now = datetime.datetime.now()
    month = now.strftime("%B")
    year = now.strftime("%Y")
    sheet_tuple = (month, "%20", year)
    sheet_name = "".join(sheet_tuple)

    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    df = pd.read_csv(url)
    for row in load_from_db():
        reapr_id = int(row[0])
        for i in df.iloc[:, 1]:
            if str(reapr_id) in str(i):
                update_db_ss(int(reapr_id))


def send_event_to_db(yt_tag, yt_datetime, yt_user, yt_msg):
    """Send new event to database and synchronize to Google Docs Spreadsheet"""
    # Contributed by johns67467
    # depends on what DB is being used.
    connection = mysql.connector.connect(
        host=db_server, user=db_user, passwd=db_passwd, db=db_name
    )
    cursor = connection.cursor()
    query = "INSERT INTO yt_events (yt_tag, yt_datetime, yt_user, yt_msg) VALUES (%s, %s, %s, %s)"

    cursor.execute(query, (yt_tag, yt_datetime, yt_user, yt_msg))
    connection.commit()
    connection.close()
    sync_ss()


def read_chat(YouTube_ID):
    """Monitor YouTube chat for new action messages"""
    chat = pytchat.create(video_id="https://www.youtube.com/watch?v=" + YouTube_ID)
    while chat.is_alive():
        for c in chat.get().sync_items():
            # Lets read all chat if we set logging to INFO
            logging.info(f"{c.datetime} [{c.author.name}]- {c.message}")
            yt_datetime = c.datetime
            yt_user = c.author.name
            yt_msg = c.message
            # See tag, label it ship it off
            tag_list = ["EVENT", "REQUEST", "THOUGHT", "FEEDBACK"]
            tag = re.findall(
                r"^#(?=(" + "|".join(tag_list) + r"):)+", c.message.upper()
            )

            if tag:
                yt_tag = tag[0]
                if yt_tag in tag_list:
                    send_event_to_db(yt_tag, yt_datetime, yt_user, yt_msg)
                    print(f"ALERT: {c.datetime} [{c.author.name}] {c.message}")
            elif not chat.is_alive:
                print("NOT is_alive caught.")
                main()


def main():
    logging.basicConfig(level=logging.ERROR)
    log = logging.getLogger()

    print("Starting REAPR - Reporting Events, Anomalous Phenomena et Requests")
    YouTube_ID = get_streamID()

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
