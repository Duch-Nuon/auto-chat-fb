#!/bin/bash

echo "🚀 Setting up Facebook Auto Chat Bot..."
echo "=================================="

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv autoChat

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source autoChat/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing Python packages..."
pip install pytz python-dotenv playwright requests

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install chromium

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOL
# Facebook Authentication Cookies
C_USER=your_c_user_value_here
XS=your_xs_value_here

# Chat Configuration
CHAT_ID=your_chat_id_here

TELEGRAM_BOT_TOKEN=7615528684
TELEGRAM_CHAT_ID=-48

EOL
    echo "✅ .env file created! Please edit it with your actual values."
else
    echo "⚠️  .env file already exists, skipping..."
fi

echo ""
echo "🎉 Setup completed successfully!"
echo "=================================="
echo "✨ Happy chatting!"