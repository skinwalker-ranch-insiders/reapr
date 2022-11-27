# REAPR - Reporting Events, Anomalous Phenomena and Requests
#
# Read chat from YouTube Live Stream and save a copy when
#      keywords are used such as #EVENT: #REQUEST: #THOUGHT:
# Created as a PoC to an idea presented by Erik Bard allowing
#      for quick, easy collection of data based on observations
#      watching the Skinwalker Insiders stream.

import sys
import time
import pytchat
import logging

print("Starting REAPR - Reporting Events, Anomalous Phenomena and Requests")

logging.basicConfig(level=logging.ERROR)
log = logging.getLogger()
YouTube_ID = " ".join(sys.argv[1:])

def SWR_YT_MSG(YT_Tag, YT_DateTime, YT_User, YT_Msg):
    # Contributed by johns67567
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
    chat = pytchat.create(video_id=YouTube_ID)
    while chat.is_alive():
        for c in chat.get().sync_items():
            # Lets read all chat if we set logging to INFO
            logging.info(f"{c.datetime} [{c.author.name}]- {c.message}")
            YT_DateTime=c.datetime
            YT_User=c.author.name
            YT_Msg=c.message
            # See tag send it somewhere. TXT for now, DB is the dream
            if c.message.startswith(('#EVENT:')):
                # Ideally this would get logged to a database
                YT_Tag='EVENT'
                SWR_YT_MSG(YT_Tag, YT_DateTime, YT_User, YT_Msg)
                print(f"EVENT: {c.datetime} [{c.author.name}] {c.message}")
            elif c.message.startswith(('#REQUEST:')):
                # Ideally this would get logged to a database
                YT_Tag='REQUEST'
                SWR_YT_MSG(YT_Tag, YT_DateTime, YT_User, YT_Msg)
                print(f"REQUEST: {c.datetime} [{c.author.name}] {c.message}")
            elif c.message.startswith(('#THOUGHT:')):
                # Ideally this would get logged to a database
                YT_Tag='THOUGHT'
                SWR_YT_MSG(YT_Tag, YT_DateTime, YT_User, YT_Msg)
                print(f"THOUGHT: {c.datetime} [{c.author.name}] {c.message}")
            elif c.message.startswith(('#ALERT:')):
                # Ideally this would trigger an email or message to someone.
                YT_Tag='ALERT'
                SWR_YT_MSG(YT_Tag, YT_DateTime, YT_User, YT_Msg)
                print(f"ALERT: {c.datetime} [{c.author.name}] {c.message}")
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

main(YouTube_ID)
