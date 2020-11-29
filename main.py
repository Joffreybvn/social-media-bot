
from src.bots import TweeterBot
import schedule

if __name__ == '__main__':

    # Instantiate the bot
    TweeterBot(20).schedule()
    print("[+] Tweeter bot started")

    # Execute the scheduled functions
    while True:
        schedule.run_pending()
