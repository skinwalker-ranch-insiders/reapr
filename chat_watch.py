import pytchat
import logging

logging.basicConfig(level=logging.INFO)

chat = pytchat.create(video_id="YT_LINK_ID")
while chat.is_alive():
    for c in chat.get().sync_items():
        logging.info(f"{c.datetime} [{c.author.name}]- {c.message}")
        if "#EVENT:" in c.message:
            with open('events.txt', 'a') as f:
                f.write(f"\nEVENT: {c.datetime} [{c.author.name}]- {c.message}")
            print(f"EVENT: {c.datetime} [{c.author.name}]- {c.message}")
        elif "#REQUEST:" in c.message:
            with open('requests.txt', 'a') as f:
                f.write(f"\nREQUEST:: {c.datetime} [{c.author.name}]- {c.message}")
            print(f"REQUEST: {c.datetime} [{c.author.name}]- {c.message}")
        elif "#THOUGHT:" in c.message:
            with open('thoughts.txt', 'a') as f:
                f.write(f"\nTHOUGHT: {c.datetime} [{c.author.name}]- {c.message}")
            print(f"THOUGHT: {c.datetime} [{c.author.name}]- {c.message}")
