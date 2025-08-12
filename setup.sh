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
EOL
    echo "✅ .env file created! Please edit it with your actual values."
else
    echo "⚠️  .env file already exists, skipping..."
fi

echo ""
echo "🎉 Setup completed successfully!"
echo "=================================="
echo ""
echo "📋 Next steps:"
echo "1. Edit the .env file with your Facebook credentials:"
echo "   - C_USER: Your Facebook c_user cookie"
echo "   - XS: Your Facebook xs cookie" 
echo "   - CHAT_ID: Target chat ID from Facebook messages URL"
echo ""
echo "2. To run the script:"
echo "   source autoChat/bin/activate"
echo "   python autoChat.py"
echo ""
echo "3. To deactivate virtual environment later:"
echo "   deactivate"
echo ""
echo "🔍 How to get Facebook credentials:"
echo "   1. Open facebook.com in browser"
echo "   2. Press F12 → Application → Cookies → facebook.com"
echo "   3. Copy 'c_user' and 'xs' values"
echo "   4. For CHAT_ID: Go to messages, open chat, copy ID from URL"
echo ""
echo "✨ Happy chatting!"