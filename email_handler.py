# email_handler.py
import imaplib
import smtplib
import email
from email.header import decode_header
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))


def fetch_prompt_from_email():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()
        print(f"📨 {len(email_ids)} unread email(s) found.")

        for email_id in reversed(email_ids):  # newest first
            print(f"🔎 Checking email ID: {email_id}")
            typ, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject_raw = msg["Subject"]
                    subject, encoding = decode_header(subject_raw)[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8")

                    print(f"📌 Subject: {subject}")

                    if "o3" in subject.lower() and "response" not in subject.lower():
                        from_ = msg.get("From")
                        body = get_email_body(msg)
                        print(f"📝 Prompt received from {from_}: {body[:60]}...")
                        mail.store(email_id, '+FLAGS', '\\Seen')  # mark as read
                        return from_, body

        mail.logout()
        return None, None

    except Exception as e:
        print(f"❌ Error while checking email: {e}")
        try:
            mail.logout()
        except:
            pass
        return None, None


def send_response_email(to_email, prompt, response):
    try:
        msg = EmailMessage()
        msg["Subject"] = "O3: Response"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email

        msg.set_content(f"🧠 Prompt:\n{prompt}\n\n🤖 Response:\n{response}")

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"📤 Email sent to {to_email}")

    except Exception as e:
        print(f"❌ Error sending email: {e}")


def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in disposition:
                try:
                    return part.get_payload(decode=True).decode()
                except:
                    continue
    else:
        try:
            return msg.get_payload(decode=True).decode()
        except:
            return ""

    return ""
