# REAPR - Reporting Events, Anomalous Phenomena and Requests
#
# Read chat from YouTube Live Stream and save a copy when
#      keywords are used such as #EVENT: #REQUEST: #THOUGHT:
# Created as a PoC to an idea presented by Erik Bard allowing
#      for quick, easy collection of data based on observations
#      watching the Skinwalker Insiders stream.

import sys
import pytchat
import logging

logging.basicConfig(level=logging.ERROR)
log = logging.getLogger()

print("Starting REAPR - Reporting Events, Anomalous Phenomena and Requests")
YouTube_ID = " ".join(sys.argv[1:])
def read_chat():
    chat = pytchat.create(video_id=YouTube_ID)
    while chat.is_alive():
        for c in chat.get().sync_items():
            # Lets read all chat if we set logging to INFO
            logging.info(f"{c.datetime} [{c.author.name}]- {c.message}")
            # See tag send it somewhere. TXT for now, DB is the dream
            if c.message.startswith(('#EVENT:')):
                with open('events.txt', 'a') as f:
                    f.write(f"\nEVENT: {c.datetime} [{c.author.name}]- {c.message}")
                print(f"EVENT: {c.datetime} [{c.author.name}] {c.message}")
            elif c.message.startswith(('#REQUEST:')):
                with open('requests.txt', 'a') as f:
                    f.write(f"\nREQUEST:: {c.datetime} [{c.author.name}]- {c.message}")
                print(f"REQUEST: {c.datetime} [{c.author.name}] {c.message}")
            elif c.message.startswith(('#THOUGHT:')):
                with open('thoughts.txt', 'a') as f:
                    f.write(f"\nTHOUGHT: {c.datetime} [{c.author.name}]- {c.message}")
                print(f"THOUGHT: {c.datetime} [{c.author.name}] {c.message}")
            
def main(YouTube_ID):
    try:
        read_chat()
    except:
        pass
main(YouTube_ID)
