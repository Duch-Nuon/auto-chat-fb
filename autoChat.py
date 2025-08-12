import os
import time as time_module
import random
from datetime import datetime, timedelta, time as dtime
import pytz
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load environment variables from .env
load_dotenv()

# Cambodia timezone
tz = pytz.timezone('Asia/Phnom_Penh')

# Wait random time between start_time and end_time
def wait_until_random_time(start_hour=15, start_minute=22, end_hour=16, end_minute=37):
    now = datetime.now(tz)
    
    # Create start and end times for today
    start = now.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)
    end = now.replace(hour=end_hour, minute=end_minute, second=0, microsecond=0)

    # If now is past the end time, schedule for next day
    if now >= end:
        start += timedelta(days=1)
        end += timedelta(days=1)
        print(f"Past end time. Scheduling for next day.")
    # If now is before start time, wait until start time today
    elif now < start:
        print(f"Before start time. Will run today between {start.strftime('%H:%M:%S')} and {end.strftime('%H:%M:%S')}")
    # If we're between start and end time, use remaining time window
    else:
        print(f"Within time window! Using remaining time until {end.strftime('%H:%M:%S')}")
        start = now  # Start from now
        # end stays the same (original end time)

    # Calculate random time within the window
    delta_seconds = int((end - start).total_seconds())
    if delta_seconds <= 0:
        print("No time remaining in window, running immediately")
        run_time = now + timedelta(seconds=2)
    else:
        random_seconds = random.randint(0, delta_seconds)
        run_time = start + timedelta(seconds=random_seconds)

    # Calculate wait time
    wait_seconds = (run_time - now).total_seconds()
    
    # Ensure wait_seconds is not negative
    if wait_seconds < 0:
        print(f"Error: Calculated negative wait time. Running immediately.")
        wait_seconds = 2  # Just wait 2 seconds
        run_time = now + timedelta(seconds=2)
    
    print(f"[{datetime.now(tz).strftime('%H:%M:%S')}] Waiting {int(wait_seconds)} seconds until {run_time.strftime('%Y-%m-%d %H:%M:%S')} to run script.")
    time_module.sleep(wait_seconds)

# Prepare Facebook cookies from environment
fb_cookies = [
    {
        "name": "c_user",
        "value": os.getenv("C_USER"),
        "domain": ".facebook.com",
        "path": "/",
        "httpOnly": True,
        "secure": True,
        "sameSite": "Lax",
    },
    {
        "name": "xs",
        "value": os.getenv("XS"),
        "domain": ".facebook.com",
        "path": "/",
        "httpOnly": True,
        "secure": True,
        "sameSite": "Lax",
    },
]

# List of messages to randomly send
ListChat = ['Hi', 'Hello', 'Bye']

def main():
    # Wait until random time in Cambodia timezone
    # For 15:22 to 15:25 (3:22 PM to 3:25 PM)
    # Will run immediately if current time is within the window
    wait_until_random_time()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        context.add_cookies(fb_cookies)
        page = context.new_page()

        chat_id = os.getenv("CHAT_ID")
        if not chat_id:
            raise ValueError("CHAT_ID is not set in environment variables!")

        url = f"https://www.facebook.com/messages/t/{chat_id}"
        page.goto(url)

        # Close popup if exists
        try:
            page.wait_for_selector('div[aria-label="Close"][role="button"]', timeout=5000)
            page.click('div[aria-label="Close"][role="button"]')
            print("Closed popup successfully!")
        except:
            print("No popup found.")

        # Wait for chat input box
        page.wait_for_selector('[contenteditable="true"]', timeout=15000)
        print("Chat loaded successfully!")

        # Send a random message
        chat_box = page.query_selector('[contenteditable="true"]')
        if chat_box:
            message = random.choice(ListChat)
            chat_box.type(message)
            time_module.sleep(5)
            chat_box.press("Enter")
            print(f"Message sent: {message}")
        else:
            print("Chat input box not found!")

        time_module.sleep(3)
        browser.close()

if __name__ == "__main__":
    main()