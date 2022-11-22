import pytchat
import logging

logging.basicConfig(level=logging.CRITICAL)

chat = pytchat.create(video_id="BdBetaZc82g")
while chat.is_alive():
    for c in chat.get().sync_items():
        logging.info(f"{c.datetime} [{c.author.name}]- {c.message}")
        if "#EVENT:" in c.message:
            print(f"EVENT: {c.datetime} [{c.author.name}]- {c.message}")
        elif "#REQUEST:" in c.message:
            print(f"REQUEST: {c.datetime} [{c.author.name}]- {c.message}")
        elif "#THOUGHT:" in c.message:
            print(f"THOUGHT: {c.datetime} [{c.author.name}]- {c.message}")
