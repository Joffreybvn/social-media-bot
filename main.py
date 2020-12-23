
from src.api import partial_run
from src.bots import TweeterBot
from threading import Thread
import schedule


if __name__ == '__main__':

    Thread(target=partial_run).start()
    print("[+] Dummy api started")

    # Instantiate the bot
    TweeterBot(60).schedule(True)
    print("[+] Tweeter bot started")

    # Execute the scheduled functions
    while True:
        schedule.run_pending()
