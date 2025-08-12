import os
import logging
from datetime import datetime
import pytz
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Cambodia timezone
tz = pytz.timezone('Asia/Phnom_Penh')

class TelegramBot:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('autochat_logs.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def send_message(self, message):
        """Send message to Telegram chat"""
        if not self.bot_token or not self.chat_id:
            self.logger.warning("Telegram bot token or chat ID not configured")
            return False
        
        url = f"{self.base_url}/sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(url, data=data, timeout=10)
            if response.status_code == 200:
                self.logger.info("Telegram notification sent successfully")
                return True
            else:
                self.logger.error(f"Failed to send Telegram message: {response.status_code}")
                return False
        except Exception as e:
            self.logger.error(f"Error sending Telegram message: {e}")
            return False
    
    def log_and_notify(self, event_type, message="", extra_info=""):
        """Log event and send Telegram notification"""
        now = datetime.now(tz)
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S %Z")
        
        # Create log message
        log_message = f"[{timestamp}] {event_type}"
        if message:
            log_message += f" - {message}"
        if extra_info:
            log_message += f" | {extra_info}"
        
        # Log to file and console
        self.logger.info(log_message)
        
        # Create Telegram message with HTML formatting
        telegram_message = (
            "🤖 <b>Auto Chat Bot Alert</b>\n\n"
            f"📅 <b>Time:</b> {timestamp}\n"
            f"🎯 <b>Event:</b> {event_type}\n"
        )
        
        if message:
            telegram_message += f"💬 <b>Message:</b> {message}\n"
        if extra_info:
            telegram_message += f"ℹ️ <b>Details:</b> {extra_info}\n"
        
        # Send notification
        self.send_message(telegram_message.strip())
    
    def notify_script_start(self, scheduled_time):
        """Notify when script starts and is scheduled"""
        self.log_and_notify(
            "SCRIPT_STARTED",
            f"Facebook auto-chat bot initialized",
            f"Scheduled to run at: {scheduled_time}"
        )
    
    def notify_message_sent(self, message, chat_target):
        """Notify when message is sent successfully"""
        self.log_and_notify(
            "MESSAGE_SENT",
            f"'{message}'",
            f"To chat: {chat_target}"
        )
    
    def notify_error(self, error_message, error_details=""):
        """Notify when an error occurs"""
        self.log_and_notify(
            "ERROR",
            error_message,
            error_details
        )
    
    def notify_script_complete(self):
        """Notify when script completes successfully"""
        self.log_and_notify(
            "SCRIPT_COMPLETED",
            "Auto-chat script finished successfully"
        )
    
    def get_bot_info(self):
        """Get bot information for testing"""
        url = f"{self.base_url}/getMe"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('result', {})
            else:
                return None
        except Exception as e:
            self.logger.error(f"Error getting bot info: {e}")
            return None

# Test function
def test_telegram_bot():
    """Test the Telegram bot functionality"""
    bot = TelegramBot()
    
    print("Testing Telegram Bot...")
    
    # Test bot info
    bot_info = bot.get_bot_info()
    if bot_info:
        print(f"✅ Bot connected: @{bot_info.get('username', 'Unknown')}")
        print(f"   Bot name: {bot_info.get('first_name', 'Unknown')}")
    else:
        print("❌ Failed to connect to bot")
        return
    
    # Test notification
    print("Sending test notification...")
    bot.log_and_notify(
        "TEST_NOTIFICATION",
        "Telegram bot is working correctly!",
        "This is a test message from your auto-chat bot"
    )
    print("✅ Test notification sent!")

if __name__ == "__main__":
    test_telegram_bot()