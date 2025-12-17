#!/bin/bash
# Installation script for Debian/Ubuntu based systems

echo "Updating package lists..."
sudo apt-get update

echo "Installing System Dependencies (WebP, ImageMagick)..."
sudo apt-get install -y webp imagemagick python3-pip python3-venv

echo "Creating Python Virtual Environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing Python Dependencies..."
pip install matplotlib

echo "Installation Complete."
echo "To run: source venv/bin/activate && python compression_analyzer.py <image>"