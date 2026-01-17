#!/bin/bash

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit .env file and add your BOT_TOKEN"
    exit 1
fi

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting bot..."
python main.py
