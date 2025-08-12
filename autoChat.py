import os
import time as time_module
import random
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from telegram_bot import TelegramBot

load_dotenv()

tz = pytz.timezone('Asia/Phnom_Penh')

telegram_bot = TelegramBot()

def wait_until_random_time(start_hour=15, start_minute=22, end_hour=17, end_minute=52):
    random.seed(int(time_module.time() * 1000) + os.getpid())
    
    now = datetime.now(tz)
    
    start = now.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)
    end = now.replace(hour=end_hour, minute=end_minute, second=0, microsecond=0)

    if now >= end:
        start += timedelta(days=1)
        end += timedelta(days=1)
        print(f"Past end time. Scheduling for next day.")
    elif now < start:
        print(f"Before start time. Will run today between {start.strftime('%H:%M:%S')} and {end.strftime('%H:%M:%S')}")
    else:
        print(f"Within time window! Using remaining time until {end.strftime('%H:%M:%S')}")
        start = now + timedelta(seconds=random.randint(1, 60))

    delta_seconds = int((end - start).total_seconds())
    print(f"Time window: {delta_seconds} seconds available")
    
    if delta_seconds <= 0:
        print("No time remaining in window, running immediately")
        run_time = now + timedelta(seconds=2)
    else:
        random_seconds = random.randint(0, delta_seconds)
        
        extra_randomness = random.uniform(-0.5, 0.5) * min(300, delta_seconds * 0.1)
        random_seconds += int(extra_randomness)
        
        random_seconds = max(0, min(random_seconds, delta_seconds))
        
        run_time = start + timedelta(seconds=random_seconds)
        print(f"Random offset: {random_seconds} seconds from start time")

    wait_seconds = (run_time - now).total_seconds()
    
    if wait_seconds < 0:
        print(f"Error: Calculated negative wait time. Running immediately.")
        wait_seconds = random.randint(2, 10)
        run_time = now + timedelta(seconds=wait_seconds)
    
    scheduled_time = run_time.strftime('%Y-%m-%d %H:%M:%S')
    wait_minutes = int(wait_seconds // 60)
    wait_seconds_remainder = int(wait_seconds % 60)
    
    print(f"[{datetime.now(tz).strftime('%H:%M:%S')}] Waiting {wait_minutes}m {wait_seconds_remainder}s until {scheduled_time} to run script.")
    print(f"Random time selected: {run_time.strftime('%H:%M:%S')} (within {start.strftime('%H:%M:%S')} - {end.strftime('%H:%M:%S')} window)")
    
    telegram_bot.notify_script_start(scheduled_time)
    
    total_wait = int(wait_seconds)
    for i in range(0, total_wait, 60):
        chunk_wait = min(60, total_wait - i)
        time_module.sleep(chunk_wait)
        remaining = total_wait - i - chunk_wait
        if remaining > 0 and remaining % 300 == 0:
            print(f"Still waiting... {remaining // 60} minutes remaining")

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

ListChat = ['Hi', 'Hello', 'Bye', 'How are you?', 'Good morning!', 'Good evening!']

def main():
    try:
        wait_until_random_time()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            context.add_cookies(fb_cookies)
            page = context.new_page()

            chat_id = os.getenv("CHAT_ID")
            if not chat_id:
                error_msg = "CHAT_ID is not set in environment variables!"
                telegram_bot.notify_error("Configuration Error", error_msg)
                raise ValueError(error_msg)

            url = f"https://www.facebook.com/messages/t/{chat_id}"
            print(f"Navigating to: {url}")
            page.goto(url, timeout=60000)

            try:
                page.wait_for_selector('div[aria-label="Close"][role="button"]', timeout=5000)
                page.click('div[aria-label="Close"][role="button"]')
                print("Closed popup successfully!")
            except:
                print("No popup found.")

            print("Waiting for chat to load...")
            page.wait_for_selector('[contenteditable="true"]', timeout=15000)
            print("Chat loaded successfully!")

            chat_box = page.query_selector('[contenteditable="true"]')
            if chat_box:
                message = random.choice(ListChat)
                print(f"Typing message: {message}")
                time_module.sleep(3)
                chat_box.type(message)
                time_module.sleep(3)
                chat_box.press("Enter")
                print(f"Message sent: {message}")
                
                telegram_bot.notify_message_sent(message, f"Chat ID: {chat_id}")
                
            else:
                error_msg = "Chat input box not found!"
                print(error_msg)
                telegram_bot.notify_error("UI Error", error_msg)

            time_module.sleep(3)
            browser.close()
            
            telegram_bot.notify_script_complete()
            print("Script completed successfully!")

    except Exception as e:
        error_msg = f"Script failed: {str(e)}"
        print(f"Error: {error_msg}")
        telegram_bot.notify_error("Script Error", error_msg)
        raise

if __name__ == "__main__":
    main()