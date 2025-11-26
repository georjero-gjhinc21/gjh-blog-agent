#!/bin/bash
# Install Node.js 18.x on Ubuntu

echo "Installing Node.js 18.x..."

# Add NodeSource repository
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -

# Install Node.js
sudo apt-get install -y nodejs

# Verify installation
echo ""
echo "Node.js version:"
node --version

echo "npm version:"
npm --version

echo ""
echo "✅ Node.js installed successfully!"
echo ""
echo "Next steps:"
echo "  cd /opt/gjh-blog-agent/frontend"
echo "  npm install"
echo "  npm run dev"
