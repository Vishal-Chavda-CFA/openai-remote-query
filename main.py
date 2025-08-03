# main.py

import time
import os
from dotenv import load_dotenv
from email_handler import fetch_prompt_from_email, send_response_email
from prompt_processor import process_prompt

load_dotenv()
DELAY = int(os.getenv("CHECK_INTERVAL", 60))  # Seconds between checks

print("📡 Starting email monitoring loop...")

while True:
    print("📥 Checking inbox for new 'O3' prompts...")
    sender, prompt = fetch_prompt_from_email()

    if sender and prompt:
        print("🤖 Sending prompt to OpenAI API...")
        try:
            response = process_prompt(prompt)
            send_response_email(sender, prompt, response)
        except Exception as e:
            print(f"❌ OpenAI API error: {e}")
            send_response_email(sender, prompt, f"Error occurred: {e}")

    time.sleep(DELAY)
