#!/usr/bin/env bash

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Install required system dependencies for Playwright
apt-get update && apt-get install -y \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxkbcommon0 \
    libgbm-dev \
    libasound2 \
    libpangocairo-1.0-0 \
    libgtk-3-0
